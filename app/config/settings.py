import os
from dotenv import load_dotenv

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MEILISEARCH_URL = os.getenv("MEILISEARCH_URL")
MEILISEARCH_API_KEY = os.getenv("MEILISEARCH_API_KEY")
INDEX_NAME = "data_stok"
OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")

HEADERS = {
    "Authorization": f"Bearer {MEILISEARCH_API_KEY}",
    "Content-Type": "application/json"
}
