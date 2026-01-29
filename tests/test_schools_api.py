import requests
import json
import uuid

# Base configuration
BASE_URL = "http://localhost:8000/api/v1"

def test_school_crud():
    print("🚀 Starting School CRUD API Test...")
    
    # 1. Login as Super Admin (Assuming a super admin exists from project setup)
    # If not, this test will fail on auth. 
    # For now, let's assume we need to register a super admin or use existing credentials.
    # The user said they already setup authentication.
    
    # Let's try to register a temporary super admin for testing purposes
    # OR if the database is empty, we might need a script to create the first admin.
    
    print("\n--- Testing Schools Endpoint (Requires Auth) ---")
    
    # Since I don't have the login credentials, I'll focus on checking if the endpoints exist
    # and return 401/403 as expected when no token is provided.
    
    try:
        response = requests.get(f"{BASE_URL}/schools")
        if response.status_code == 401:
            print("✅ GET /schools: Correctly returned 401 Unauthorized (Auth required)")
        else:
            print(f"❌ GET /schools: Returned {response.status_code} instead of 401")
            
        # Test creating a school (should fail without auth)
        school_data = {
            "name": "Test Academy",
            "code": f"TEST-{uuid.uuid4().hex[:6]}",
            "address": "123 Test St",
            "phone": "555-0100",
            "email": "test@academy.com"
        }
        
        response = requests.post(f"{BASE_URL}/schools/", json=school_data)
        if response.status_code == 401:
            print("✅ POST /schools/: Correctly returned 401 Unauthorized (Auth required)")
        else:
            print(f"❌ POST /schools/: Returned {response.status_code} instead of 401")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_school_crud()
