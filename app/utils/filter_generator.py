import google.generativeai as genai
import streamlit as st
from config.settings import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def generate_filter(question: str):
    prompt = """
        Buatkan filter MeiliSearch untuk pertanyaan stok kain dengan format:
        nama_kain = '{nama_kain}' AND jenis_warna = '{jenis_warna}' AND cabang = '{cabang}'.
        Kecualikan kain `RIB`, `KRAH`, `Manset` dengan `nama_kain NOT CONTAINS`.
        Jika pertanyaan bukan tentang stok, balas "greetings".
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, question])
        return response.text.strip() if response.text.strip() != "greetings" else None
    except Exception as e:
        st.error(f"Error generating filter: {e}")
        return None
