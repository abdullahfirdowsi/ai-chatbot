#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

def test_grok_api():
    """Test the Grok API integration"""
    try:
        # Initialize client
        client = Groq(api_key=os.getenv("API_KEY"))
        model_name = os.getenv("MODEL_NAME", "gemma2-9b-it")
        
        print(f"Testing Grok API with model: {model_name}")
        print(f"API Key loaded: {'✓' if os.getenv('API_KEY') else '✗'}")
        
        # Test message
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful AI tutor. Respond briefly and enthusiastically."
                },
                {
                    "role": "user", 
                    "content": "Hi! Can you help me learn about photosynthesis?"
                }
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        if response.choices:
            print("✓ API call successful!")
            print(f"Response: {response.choices[0].message.content}")
            return True
        else:
            print("✗ No response received")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_grok_api()
