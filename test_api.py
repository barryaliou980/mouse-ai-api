#!/usr/bin/env python3
"""
Test script for the Mouse AI API.
"""
import requests
import json
import time

def test_health_endpoint():
    """Test the health endpoint."""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_move_endpoint():
    """Test the move endpoint."""
    try:
        # Test data matching frontend format
        test_data = {
            "mouseId": "test-mouse-1",
            "position": {"x": 1, "y": 1},
            "environment": {
                "grid": [
                    ["wall", "wall", "wall", "wall"],
                    ["wall", "path", "path", "wall"],
                    ["wall", "path", "cheese", "wall"],
                    ["wall", "wall", "wall", "wall"]
                ],
                "width": 4,
                "height": 4,
                "cheesePositions": [{"x": 2, "y": 2}],
                "otherMice": [],
                "walls": [],
                "paths": []
            },
            "mouseState": {
                "health": 100,
                "happiness": 80,
                "energy": 90,
                "cheeseFound": 0
            },
            "availableMoves": ["north", "south", "east", "west"]
        }
        
        response = requests.post(
            "http://localhost:8000/api/move",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"Move request: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Move request failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Mouse AI API...")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("Waiting for server to start...")
    time.sleep(2)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    # Test move endpoint
    print("\n2. Testing move endpoint...")
    move_ok = test_move_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Health endpoint: {'✓' if health_ok else '✗'}")
    print(f"Move endpoint: {'✓' if move_ok else '✗'}")
    
    if health_ok and move_ok:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main()
