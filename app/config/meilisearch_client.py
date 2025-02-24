import meilisearch
from app.config.settings import MEILISEARCH_URL, MEILISEARCH_API_KEY

meiliClient = meilisearch.Client(MEILISEARCH_URL, MEILISEARCH_API_KEY)
