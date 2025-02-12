import requests
import os
from dotenv import load_dotenv

load_dotenv()

MEILISEARCH_URL = os.getenv("MEILISEARCH_URL")
MEILISEARCH_API_KEY = os.getenv("MEILISEARCH_API_KEY")
INDEX_NAME = "data_stok"

headers = {
    "Authorization": f"Bearer {MEILISEARCH_API_KEY}",
    "Content-Type": "application/json"
}

def search_meilisearch(query_filter):
    try:
        url = f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/search"
        payload = {
            "q": "",
            "filter": query_filter
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("hits", [])
    except requests.RequestException as e:
        return f"Error querying MeiliSearch: {e}"
