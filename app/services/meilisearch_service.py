import requests
import streamlit as st
from config.settings import MEILISEARCH_URL, INDEX_NAME, HEADERS

def search_meilisearch(query_filter):
    try:
        url = f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/search"
        payload = {"q": "", "filter": query_filter}
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("hits", [])
    except requests.RequestException as e:
        st.error(f"Error querying MeiliSearch: {e}")
        return []
