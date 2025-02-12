import faiss
import os
import re
import numpy as np
import pickle
import streamlit as st
from sentence_transformers import SentenceTransformer
from transformers import pipeline

encoder = SentenceTransformer("all-MiniLM-L6-v2")
intent_classifier = pipeline(
    "zero-shot-classification", model="facebook/bart-large-mnli"
)

SAVE_DIR = "app/data/"
index_path = os.path.join(SAVE_DIR, "kanita_faiss.index")
texts_path = os.path.join(SAVE_DIR, "kanita_texts.pkl")
intents_path = os.path.join(SAVE_DIR, "kanita_intents.pkl")

os.makedirs(SAVE_DIR, exist_ok=True)


def clean_text(text):
    """Membersihkan teks: lowercase, hapus emoji & karakter khusus."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


@st.cache_resource
def load_faiss_index():
    """Memuat FAISS index hanya sekali."""
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index tidak ditemukan di {index_path}")

    index = faiss.read_index(index_path)

    with open(texts_path, "rb") as f:
        knowledge_texts = pickle.load(f)

    with open(intents_path, "rb") as f:
        knowledge_intents = pickle.load(f)

    return index, knowledge_texts, knowledge_intents


index, knowledge_texts, knowledge_intents = load_faiss_index()


def detect_intent(query):
    """Mendeteksi intent dari query menggunakan model zero-shot classification."""
    intent_labels = list(set(knowledge_intents))

    result = intent_classifier(query, intent_labels)
    detected_intent = result["labels"][0]

    return detected_intent


def retrieve_relevant_context(query, top_k=3, score_threshold=0.6):
    """Mencari konteks yang paling relevan berdasarkan FAISS index."""
    query = clean_text(query)
    detected_intent = detect_intent(query)
    query_embedding = encoder.encode([query])
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    if index.ntotal == 0:
        return []

    top_k = min(top_k, index.ntotal)
    distances, indices = index.search(query_embedding.astype(np.float32), top_k)

    results = []
    for i, distance in zip(indices[0], distances[0]):
        similarity = 1 / (1 + distance)
        if similarity >= score_threshold:
            results.append((knowledge_texts[i], knowledge_intents[i], similarity))

    results.sort(key=lambda x: x[2], reverse=True)

    return results, detected_intent
