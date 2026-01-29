import requests
import json
import uuid

# Base configuration
BASE_URL = "http://localhost:8000/api/v1"

def test_academic_management_api():
    print("🚀 Starting Academic Management API Verification...")
    
    endpoints = [
        ("GET", "/academic/years"),
        ("POST", "/academic/years"),
        ("POST", "/academic/terms"),
        ("GET", "/academic/classrooms"),
        ("POST", "/students/"),
        ("GET", "/students/"),
        ("POST", "/subjects/"),
        ("POST", "/subjects/assign-teacher"),
    ]
    
    print("\n--- Testing Protection (Should be 401/403 without token) ---")
    for method, endpoint in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json={})
                
            status = response.status_code
            if status in [401, 403]:
                print(f"✅ {method} {endpoint}: Correctly protected ({status})")
            else:
                print(f"⚠️ {method} {endpoint}: Returned {status}")
                
        except Exception as e:
            print(f"❌ {method} {endpoint}: Connection error - {e}")

if __name__ == "__main__":
    test_academic_management_api()
    print("\n💡 Tip: Use /docs to test with a logged-in Super Admin token.")
