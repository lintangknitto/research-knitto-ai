from config.meilisearch_client import meiliClient
import re
from utils.pre_processing import pre_processing


def get_data_meili(type: str):
    index = meiliClient.index("kamus_kata")
    filter_cond = f"""type = '{type}'"""
    search_results = index.search("", {"filter": filter_cond, "limit": 1000})

    # Returning the words in a set and converting them to lowercase
    return set(result["word"].lower() for result in search_results["hits"])

# Function to extract and aggregate all valid words into a single dictionary
def extract_valid_text_from_dict(text=""):
    dictionary = {}
    types = ['kain', 'warna']  # Add more types here if needed
    combined_data = set()

    # Loop through each type and combine valid words into one set
    for t in types:
        data = get_data_meili(t)
        combined_data.update(data)

    dictionary["valid_words"] = combined_data

    return dictionary


teks = 'saya ingin membeli combed 30s'
tokens = pre_processing(text=teks)

print(tokens)