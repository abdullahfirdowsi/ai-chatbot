from fastapi import APIRouter, HTTPException
from app.models import ChatMessage
from app.database import messages_col
import os
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import logging

# Load environment variables
load_dotenv()

router = APIRouter()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME", "gemma2-9b-it")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback responses for when API fails
FALLBACK_RESPONSES = [
    "I'm here to help you learn! Can you tell me more about what you'd like to understand?",
    "That's an interesting question! Let me think about the best way to explain this to you.",
    "I love that you're curious about learning! What specific aspect would you like to explore?",
    "Great question! Let's work through this together step by step."
]

@router.post("/chat")
async def chat_endpoint(chat: ChatMessage):
    try:
        if not chat.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Save user message with timestamp
        user_message = {
            "text": chat.message,
            "sender": "user",
            "timestamp": datetime.utcnow()
        }
        messages_col.insert_one(user_message)

        # Generate intelligent tutor response
        bot_reply = generate_tutor_response(chat.message)

        # Save bot reply with timestamp
        bot_message = {
            "text": bot_reply,
            "sender": "bot",
            "timestamp": datetime.utcnow()
        }
        messages_col.insert_one(bot_message)

        return {"reply": bot_reply}
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Sorry, I encountered an error. Please try again.")

def generate_tutor_response(user_message: str) -> str:
    """Generate AI tutor responses using Grok API"""
    try:
        # Create a system prompt that defines the AI tutor's personality and approach
        system_prompt = """
You are VizTalk, an intelligent AI tutor designed to help students learn effectively. Your personality is:
- Encouraging and supportive
- Patient and understanding
- Clear in explanations
- Enthusiastic about learning
- Able to break down complex topics into simple steps
- Always asking follow-up questions to ensure understanding

Your teaching approach:
- Use the Socratic method when appropriate
- Provide examples and analogies
- Encourage critical thinking
- Adapt your language to the student's level
- Make learning engaging and fun
- Always be positive and motivating

Keep your responses conversational, helpful, and educational. If you don't know something, admit it and suggest how the student might find the answer.
        """.strip()
        
        # Make API call to Grok
        logger.info(f"Making API call to Grok for message: {user_message[:50]}...")
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=500,
            temperature=0.7,
            top_p=0.9
        )
        
        # Extract the response
        if response.choices and len(response.choices) > 0:
            ai_response = response.choices[0].message.content.strip()
            logger.info("Successfully generated response from Grok API")
            return ai_response
        else:
            logger.warning("No response choices returned from API")
            return "I'm here to help you learn! What would you like to explore today?"
            
    except Exception as e:
        logger.error(f"Error calling Grok API: {str(e)}")
        # Fallback to a simple response if API fails
        import random
        return random.choice(FALLBACK_RESPONSES)

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "VizTalk AI Tutor Backend"}

@router.get("/")
async def root():
    return {
        "message": "Welcome to VizTalk AI Tutor Backend!",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send chat message",
            "/health": "GET - Health check",
            "/": "GET - API info"
        }
    }
