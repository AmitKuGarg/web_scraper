import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
