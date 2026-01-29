import requests
from datetime import datetime

# Base configuration
BASE_URL = "http://localhost:8000/api/v1"

def test_performance_management_api():
    print("🚀 Starting Attendance & Grades API Verification...")
    
    endpoints = [
        ("POST", "/attendance/bulk"),
        ("GET", "/attendance/classroom/"),
        ("POST", "/grades/assessments"),
        ("POST", "/grades/bulk-enter"),
        ("GET", "/reports/report-card/"),
    ]
    
    print("\n--- Testing Protection (Should be 401/403 without token) ---")
    for method, endpoint in endpoints:
        try:
            # Adding a dummy UUID for GET endpoints that require it
            test_endpoint = endpoint if not endpoint.endswith("/") else f"{endpoint}00000000-0000-0000-0000-000000000000"
            
            if method == "GET":
                response = requests.get(f"{BASE_URL}{test_endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{test_endpoint}", json={})
                
            status = response.status_code
            if status in [401, 403]:
                print(f"✅ {method} {endpoint}: Correctly protected ({status})")
            else:
                print(f"⚠️ {method} {endpoint}: Returned {status}")
                
        except Exception as e:
            print(f"❌ {method} {endpoint}: Connection error - {e}")

if __name__ == "__main__":
    test_performance_management_api()
    print("\n💡 Tip: Use /docs to test PDF generation with a valid token.")
