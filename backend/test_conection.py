from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get credentials from .env
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("Testing Supabase connection...")
print(f"URL: {url}")
print(f"Key: {key[:20]}...")

try:
    # Create Supabase client
    supabase: Client = create_client(url, key)
    
    # Test query
    response = supabase.table("schools").select("*").limit(1).execute()
    
    print("✅ Connection successful!")
    print(f"Schools table exists and is accessible")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")