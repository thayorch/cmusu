import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client | None = None

if not url or not key:
    print("⚠️  Warning: SUPABASE_URL or SUPABASE_KEY is missing in .env file!")
else:
    supabase = create_client(url, key)
    print("✅ Successfully connected to Supabase!")