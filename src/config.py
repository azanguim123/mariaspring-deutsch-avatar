import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
ASSETS_DIR = BASE_DIR / os.getenv("ASSETS_DIR", "assets")
DEFAULT_LEVEL = os.getenv("DEFAULT_LEVEL", "A1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")