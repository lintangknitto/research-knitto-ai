# import re
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer
# import pickle
# import os
# from app.utils.memory import KANITA_MEMORY

# encoder = SentenceTransformer("all-MiniLM-L6-v2")

# SAVE_DIR = "app/data/"
# index_path = os.path.join(SAVE_DIR, "kanita_faiss.index")
# texts_path = os.path.join(SAVE_DIR, "kanita_texts.pkl")
# intents_path = os.path.join(SAVE_DIR, "kanita_intents.pkl")

# os.makedirs(SAVE_DIR, exist_ok=True)


# def clean_text(text):
#     """Membersihkan teks: lowercase, hapus emoji & karakter khusus."""
#     text = text.lower().strip()
#     text = re.sub(r"[^\w\s]", "", text)  # Hapus karakter selain huruf/angka
#     return text


# # Preprocess data
# knowledge_texts = [clean_text(text) for _, text in KANITA_MEMORY]
# knowledge_intents = [intent for intent, _ in KANITA_MEMORY]

# # Encode teks ke vektor
# knowledge_embeddings = encoder.encode(knowledge_texts)
# knowledge_embeddings = knowledge_embeddings / np.linalg.norm(
#     knowledge_embeddings, axis=1, keepdims=True
# )  # Normalisasi

# # Buat FAISS index dengan HNSW
# dimension = knowledge_embeddings.shape[1]
# index = faiss.IndexHNSWFlat(dimension, 32)
# index.add(knowledge_embeddings.astype(np.float32))

# # Simpan FAISS index & data teks
# faiss.write_index(index, index_path)

# with open(texts_path, "wb") as f:
#     pickle.dump(knowledge_texts, f)

# with open(intents_path, "wb") as f:
#     pickle.dump(knowledge_intents, f)

# print(f"✅ FAISS index saved at: {index_path}")
# print(f"✅ Knowledge texts saved at: {texts_path}")
# print(f"✅ Knowledge intents saved at: {intents_path}")
