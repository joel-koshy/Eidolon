"""
Setup script for Gemini API configuration.
Run this script to set up your GEMINI_API_KEY environment variable.
"""

import os
import sys

def check_api_key():
    """Check if GEMINI_API_KEY is set in environment."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✓ GEMINI_API_KEY is set in environment")
        print(f"  Key preview: {api_key[:10]}...{api_key[-4:]}")
        return True
    else:
        print("✗ GEMINI_API_KEY is not set")
        return False

def test_api_connection():
    """Test connection to Gemini API."""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("✗ Cannot test: API key not set")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro-latest')
        
        # Simple test
        response = model.generate_content("Say 'OK' if you can hear me.")
        print("✓ API connection successful!")
        print(f"  Test response: {response.text.strip()}")
        return True
        
    except ImportError:
        print("✗ google-generativeai package not installed")
        print("  Install with: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"✗ API connection failed: {e}")
        return False

def main():
    print("=" * 60)
    print("GEMINI API SETUP")
    print("=" * 60)
    print()
    
    # Check if key exists
    has_key = check_api_key()
    print()
    
    if not has_key:
        print("To set up your API key:")
        print()
        print("1. Get your API key from: https://aistudio.google.com/app/apikey")
        print()
        print("2. Set it as an environment variable:")
        print()
        print("   Windows (PowerShell):")
        print("   $env:GEMINI_API_KEY='your-api-key-here'")
        print()
        print("   Windows (Command Prompt):")
        print("   set GEMINI_API_KEY=your-api-key-here")
        print()
        print("   For permanent setup, add to System Environment Variables")
        print()
        sys.exit(1)
    
    # Test connection
    print("Testing API connection...")
    test_api_connection()
    print()
    print("=" * 60)
    print("Setup complete! You're ready to use the video improver.")
    print("=" * 60)

if __name__ == "__main__":
    main()
