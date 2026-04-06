import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class CsrfSettings(BaseModel):
    secret_key: str = os.getenv("CSRF_SECRET_KEY", "fallback-secret-key")