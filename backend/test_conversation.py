#!/usr/bin/env python3

import asyncio
from app.routes import generate_tutor_response
from app.database import messages_col

async def test_conversation_flow():
    """Test the conversation flow to ensure VizTalk only introduces itself once"""
    
    # Clear any existing conversation
    messages_col.delete_many({})
    print("🧹 Cleared conversation history\n")
    
    # Test messages
    test_messages = [
        "hi",
        "what is AI",
        "ok"
    ]
    
    print("🤖 Testing conversation flow:\n")
    print("="*60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n👤 User: {message}")
        
        # Save user message to database (simulating the API endpoint)
        from datetime import datetime
        user_msg = {
            "text": message,
            "sender": "user", 
            "timestamp": datetime.utcnow()
        }
        messages_col.insert_one(user_msg)
        
        # Get bot response
        response = await generate_tutor_response(message)
        
        # Save bot response to database
        bot_msg = {
            "text": response,
            "sender": "bot",
            "timestamp": datetime.utcnow()
        }
        messages_col.insert_one(bot_msg)
        
        print(f"🤖 VizTalk: {response}")
        
        if i == 1:
            # Check if first response contains introduction
            if "I'm VizTalk" in response:
                print("✅ First message: Introduction present")
            else:
                print("⚠️  First message: Introduction missing")
        else:
            # Check if subsequent responses don't contain introduction
            if "I'm VizTalk" in response:
                print("❌ Subsequent message: Unwanted introduction present")
            else:
                print("✅ Subsequent message: No unwanted introduction")
        
        print("-" * 60)
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    asyncio.run(test_conversation_flow())
