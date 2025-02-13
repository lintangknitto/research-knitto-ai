import meilisearch
from config.settings import MEILISEARCH_URL, MEILISEARCH_API_KEY

client = meilisearch.Client(MEILISEARCH_URL, MEILISEARCH_API_KEY)

def get_memory_from_meili(intent: str):
    """Mengambil data dari MeiliSearch berdasarkan intent yang diberikan sebagai nama indeks."""
    
    try:
        index = client.index(intent)
        
        results = index.search("")

        return results['hits'] 

    except Exception as e:
        return f"Terjadi kesalahan saat mengambil data dari MeiliSearch: {e}"

intent = "stok" 
memory_data = get_memory_from_meili(intent)

print(memory_data)
