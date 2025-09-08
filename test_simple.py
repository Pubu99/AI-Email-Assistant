"""
Simple test for the basic MLOps setup
"""
import requests
import time

def test_simple_api():
    """Test the simplified API"""
    base_url = "http://localhost:8000"
    
    print("=== Testing Simple MLOps Setup ===")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✓ Health check: {response.status_code}")
        if response.status_code == 200:
            health = response.json()
            print(f"  Status: {health['status']}")
            print(f"  Version: {health['version']}")
        else:
            print(f"✗ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✓ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            root = response.json()
            print(f"  Message: {root['message']}")
    except Exception as e:
        print(f"✗ Root endpoint error: {e}")
    
    # Test prediction endpoint
    try:
        test_email = {
            "email": "Hello, I have a question about my order. Can you help me?"
        }
        response = requests.post(f"{base_url}/predict", json=test_email, timeout=10)
        print(f"✓ Prediction endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Intent: {result.get('intent')}")
            print(f"  Reply: {result.get('reply')[:50]}...")
        else:
            print(f"✗ Prediction failed: {response.text}")
    except Exception as e:
        print(f"✗ Prediction error: {e}")
    
    print("\n=== Simple MLOps Test Complete ===")
    return True

if __name__ == "__main__":
    test_simple_api()
