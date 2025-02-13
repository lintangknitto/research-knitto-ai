from config.model_client import MODEL
import streamlit as st


def detect_intent(question: str):
    prompt = """
        Kamu adalah asisten virtual yang bertugas mendeteksi intent dari pertanyaan pengguna dalam bahasa Indonesia.
        Berikut adalah daftar intent yang tersedia:
        - greetings: jika pengguna memberikan sapaan seperti "halo", "hi", "selamat pagi", atau mengenalkan dirinya.
        - thanks: jika pengguna mengucapkan terima kasih seperti "terima kasih", "makasih", atau sejenisnya.
        - stok: jika pengguna bertanya tentang stok kain.
        - faq: jika pengguna bertanya tentang layanan, bantuan, cabang, atau informasi umum seputar Knitto Textile.
        - cek_resi: jika pengguna bertanya yang berkaitan dengan resi.
        - status_order: jika pengguna bertanya yang berkaitan dengan status order.
        - price_list: jika pengguna bertanya tentang semua yang berkaitan dengan price list, harga atau yang serupa.
        - kanita: jika pengguna bertanya tentang diri kamu atau identitas kamu.
        - unknown: jika pertanyaan tidak cocok dengan intent di atas.

        Balas hanya dengan satu kata intent dari daftar di atas, tanpa tambahan kata atau penjelasan. Jangan pernah membuat intens selain diatas
    """
    try:
        response = MODEL.generate_content([prompt, question])
        return response.text.strip().lower()
    except Exception as e:
        st.error(f"Error detecting intent: {e}")
        return "unknown"
