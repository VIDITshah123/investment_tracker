import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")
SCREENER_EMAIL = os.getenv("SCREENER_EMAIL", "")
SCREENER_PASSWORD = os.getenv("SCREENER_PASSWORD", "")
SCREENER_URL = os.getenv("SCREENER_URL", "https://www.screener.in/screens/3776183/pratik-bohra/")

DB_PATH = BASE_DIR / os.getenv("DB_PATH", "database/pbeip.db")
DATA_PATH = BASE_DIR / os.getenv("DATA_PATH", "data")
LOGS_PATH = BASE_DIR / "logs"
BACKUPS_PATH = BASE_DIR / "backups"

# Ensure directories exist
DATA_PATH.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)
BACKUPS_PATH.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "database").mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

# AI / Scoring Defaults
DEFAULT_MODEL = "gpt-4o"
HF_MODEL = "Qwen/Qwen2.5-72B-Instruct"  # High performance open-source LLM on Hugging Face Inference API
MAX_TOKENS = 4000
