import google.generativeai as genai
import streamlit as st
from config.settings import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)


def detect_intent(question: str):
    prompt = """
        Kamu adalah asisten virtual yang bertugas mendeteksi intent dari pertanyaan pengguna dalam bahasa Indonesia.
        Berikut adalah daftar intent yang tersedia:
        - greetings: jika pengguna memberikan sapaan seperti "halo", "hi", "selamat pagi", atau mengenalkan dirinya.
        - thanks: jika pengguna mengucapkan terima kasih seperti "terima kasih", "makasih", atau sejenisnya.
        - stok: jika pengguna bertanya tentang stok kain.
        - jenis_kain: jika pengguna bertanya tentang jenis kain, warna kain, spesifikasi kain, atau kualitasnya.
        - profile: jika pengguna bertanya tentang siapa kamu atau ingin mengetahui tentang Kanita.
        - help_info: jika pengguna bertanya tentang layanan, bantuan, cabang, atau informasi umum seputar Knitto Textile.
        - unknown: jika pertanyaan tidak cocok dengan intent di atas.

        Balas hanya dengan satu kata intent dari daftar di atas, tanpa tambahan kata atau penjelasan.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt, question])
        return response.text.strip().lower()
    except Exception as e:
        st.error(f"Error detecting intent: {e}")
        return "unknown"
