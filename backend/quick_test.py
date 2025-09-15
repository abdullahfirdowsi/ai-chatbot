#!/usr/bin/env python3

# Quick test to see if our imports work
try:
    print("Testing imports...")
    from app.routes import generate_tutor_response
    print("✓ Routes imported successfully")
    
    # Test the function directly
    print("Testing Grok API call...")
    response = generate_tutor_response("Hello! Can you help me learn about math?")
    print(f"✓ Response received: {response}")
    
    print("\n🎉 Integration successful!")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
