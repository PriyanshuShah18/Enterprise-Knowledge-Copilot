import os

#print("CWD:", os.getcwd())

from dotenv import load_dotenv

load_dotenv()
#print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")



if not GOOGLE_API_KEY and not GROQ_API_KEY:
    raise RuntimeError(
        "At least one LLM API key must be set"
    )

UPLOAD_DIR = "data/uploads"
