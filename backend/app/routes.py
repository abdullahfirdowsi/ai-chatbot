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
    api_key=os.getenv("AI_CHATBOT_API_KEY")
)

MODEL_NAME = os.getenv("AI_CHATBOT_MODEL_NAME", "gemma2-9b-it")

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

        # Generate intelligent tutor response with conversation context
        bot_reply = await generate_tutor_response(chat.message)

        # Save bot reply with timestamp
        bot_message = {
            "text": bot_reply,
            "sender": "bot",
            "timestamp": datetime.utcnow()
        }
        messages_col.insert_one(bot_message)

        return {"reply": bot_reply}
    
    except Exception as e:
        logger.error(f"AI Chatbot - Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Sorry, I encountered an error. Please try again.")

async def generate_tutor_response(user_message: str) -> str:
    """Generate AI Chatbot responses using Grok API with conversation context"""
    try:
        # Get conversation history (last 10 messages for context)
        recent_messages = list(messages_col.find().sort("timestamp", -1).limit(10))
        recent_messages.reverse()  # Put in chronological order
        
        # Check if this is the first interaction (no previous bot messages)
        is_first_interaction = not any(msg["sender"] == "bot" for msg in recent_messages)
        
        # Create conversation context
        conversation_messages = []
        
        # System prompt that adapts based on whether it's the first interaction
        if is_first_interaction:
            system_prompt = """
You are AI Chatbot, an intelligent AI tutor. This is your FIRST interaction with this student.

For this FIRST message only, introduce yourself briefly as "Hi there! I'm AI Chatbot, your friendly AI tutor" and then proceed to help with their question.

Your personality:
- Encouraging and supportive
- Patient and understanding  
- Clear in explanations
- Enthusiastic about learning
- Ask follow-up questions to ensure understanding

Your teaching approach:
- Use examples and analogies
- Encourage critical thinking
- Adapt language to student's level
- Make learning engaging and fun
- Be positive and motivating

IMPORTANT FORMATTING: Always format your responses using Markdown syntax:
- Use **bold** for important terms or emphasis
- Use *italics* for subtle emphasis
- Use bullet points with * for lists
- Use numbered lists when showing steps
- Use `code` formatting for technical terms
- Use proper headings with # when needed
- Use > for quotes or important notes

Keep responses conversational, helpful, and educational.
            """.strip()
        else:
            system_prompt = """
You are AI Chatbot, an AI tutor continuing an ongoing conversation with a student.

DO NOT introduce yourself again - you've already met this student.
Simply continue the conversation naturally and helpfully.

Your personality:
- Encouraging and supportive
- Patient and understanding
- Clear in explanations
- Enthusiastic about learning
- Ask follow-up questions to ensure understanding

Your teaching approach:
- Use examples and analogies
- Encourage critical thinking
- Adapt language to student's level
- Make learning engaging and fun
- Be positive and motivating

IMPORTANT FORMATTING: Always format your responses using Markdown syntax:
- Use **bold** for important terms or emphasis
- Use *italics* for subtle emphasis
- Use bullet points with * for lists
- Use numbered lists when showing steps
- Use `code` formatting for technical terms
- Use proper headings with # when needed
- Use > for quotes or important notes

Keep responses conversational, helpful, and educational.
            """.strip()
        
        conversation_messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # Add recent conversation history for context (skip system messages)
        for msg in recent_messages[-6:]:  # Last 6 messages for context
            if msg["sender"] == "user":
                conversation_messages.append({
                    "role": "user", 
                    "content": msg["text"]
                })
            elif msg["sender"] == "bot":
                conversation_messages.append({
                    "role": "assistant",
                    "content": msg["text"]
                })
        
        # Add the current user message
        conversation_messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Make API call to Grok
        logger.info(f"AI Chatbot - Making API call to Grok for message: {user_message[:50]}... (First interaction: {is_first_interaction})")
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation_messages,
            max_tokens=500,
            temperature=0.7,
            top_p=0.9
        )
        
        # Extract the response
        if response.choices and len(response.choices) > 0:
            ai_response = response.choices[0].message.content.strip()
            logger.info("AI Chatbot - Successfully generated response from Grok API")
            return ai_response
        else:
            logger.warning("AI Chatbot - No response choices returned from API")
            return "I'm here to help you learn! What would you like to explore today?"
            
    except Exception as e:
        logger.error(f"AI Chatbot - Error calling Grok API: {str(e)}")
        # Fallback to a simple response if API fails
        import random
        return random.choice(FALLBACK_RESPONSES)

@router.delete("/chat/clear")
async def clear_conversation():
    """Clear conversation history"""
    try:
        messages_col.delete_many({})
        return {"message": "Conversation history cleared successfully"}
    except Exception as e:
        logger.error(f"AI Chatbot - Error clearing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear conversation")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Chatbot Backend"}

@router.get("/")
async def root():
    return {
        "message": "Welcome to AI Chatbot Backend!",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send chat message",
            "/chat/clear": "DELETE - Clear conversation history",
            "/health": "GET - Health check",
            "/": "GET - API info"
        }
    }
