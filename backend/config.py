import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMAIL_TOKEN = os.getenv("GMAIL_TOKEN")
DB_URI = os.getenv("MONGO_URI")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment")

load_dotenv(dotenv_path=".env")
