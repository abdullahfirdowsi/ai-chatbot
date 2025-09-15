#!/usr/bin/env python3
"""
Test script for AI Chatbot Backend API
Tests the basic functionality and verifies the new branding is working correctly.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            assert "AI Chatbot Backend" in data.get("service", "")
            print("✅ Service name correctly shows 'AI Chatbot Backend'")
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed with error: {e}")
        return False
    return True

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint passed: {data}")
            assert "AI Chatbot Backend" in data.get("message", "")
            print("✅ Welcome message correctly shows 'AI Chatbot Backend'")
        else:
            print(f"❌ Root endpoint failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint failed with error: {e}")
        return False
    return True

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("\nTesting chat endpoint...")
    try:
        # Test with a simple message
        payload = {"message": "Hello, can you help me?"}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(f"{BASE_URL}/chat", 
                               data=json.dumps(payload), 
                               headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("reply", "")
            print(f"✅ Chat endpoint passed")
            print(f"📝 Response: {reply[:100]}...")
            
            # Check if the response contains AI Chatbot branding
            if "AI Chatbot" in reply:
                print("✅ Response correctly identifies as 'AI Chatbot'")
            else:
                print("⚠️  Response doesn't explicitly mention 'AI Chatbot' (this might be OK depending on the AI's response)")
                
        else:
            print(f"❌ Chat endpoint failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat endpoint failed with error: {e}")
        return False
    return True

def test_clear_conversation():
    """Test the clear conversation endpoint"""
    print("\nTesting clear conversation endpoint...")
    try:
        response = requests.delete(f"{BASE_URL}/chat/clear")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Clear conversation passed: {data}")
        else:
            print(f"❌ Clear conversation failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Clear conversation failed with error: {e}")
        return False
    return True

def main():
    """Run all tests"""
    print("🚀 Starting AI Chatbot Backend API Tests\n")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv("AI_CHATBOT_API_KEY")
    model_name = os.getenv("AI_CHATBOT_MODEL_NAME")
    
    if api_key:
        print(f"✅ AI_CHATBOT_API_KEY is configured")
    else:
        print("⚠️  AI_CHATBOT_API_KEY is not set")
    
    if model_name:
        print(f"✅ AI_CHATBOT_MODEL_NAME is configured: {model_name}")
    else:
        print("⚠️  AI_CHATBOT_MODEL_NAME is not set")
    
    print("=" * 50)
    
    tests = [
        test_health_endpoint,
        test_root_endpoint,
        test_chat_endpoint,
        test_clear_conversation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! AI Chatbot backend is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the server and configuration.")

if __name__ == "__main__":
    main()
