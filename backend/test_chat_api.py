#!/usr/bin/env python3

import requests
import time
import subprocess
import sys
from threading import Thread

def start_server():
    """Start the server in background"""
    try:
        subprocess.Popen([
            sys.executable, "start_server.py"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Give server time to start
    except Exception as e:
        print(f"Error starting server: {e}")

def test_chat_endpoint():
    """Test the chat endpoint"""
    try:
        # Test health endpoint first
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✓ Server is running")
        else:
            print("✗ Server health check failed")
            return False
            
        # Test chat endpoint
        chat_data = {
            "message": "Hello! Can you explain what photosynthesis is?"
        }
        
        print("Sending test message to chat API...")
        chat_response = requests.post(
            "http://localhost:8000/chat", 
            json=chat_data,
            timeout=30
        )
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            print("✓ Chat API call successful!")
            print(f"Response: {result.get('reply', 'No reply found')}")
            return True
        else:
            print(f"✗ Chat API failed with status: {chat_response.status_code}")
            print(f"Error: {chat_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        return False
    except requests.exceptions.Timeout:
        print("✗ Request timed out")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Chat API Integration...")
    
    # Start server
    start_server()
    
    # Test endpoint
    success = test_chat_endpoint()
    
    if success:
        print("\n🎉 All tests passed! Your chatbot is now using Grok API!")
    else:
        print("\n❌ Tests failed. Check the server logs for more details.")
