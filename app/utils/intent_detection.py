from config.model_client import AIModels
import streamlit as st


def detect_intent(question: str):
    prompt = """
        Kamu adalah asisten virtual yang bertugas mendeteksi intent dari pertanyaan pengguna dalam bahasa Indonesia.
        Berikut adalah daftar intent yang tersedia:
        - greetings: jika pengguna memberikan sapaan seperti "halo", "hi", "selamat pagi", atau mengenalkan dirinya.
        - thanks: jika pengguna mengucapkan terima kasih seperti "terima kasih", "makasih", atau sejenisnya.
        - stok: jika pengguna bertanya tentang stok kain.
        - faq: jika pengguna bertanya tentang layanan, bantuan, cabang, cara order, atau informasi umum seputar Knitto Textile.
        - cek_resi: jika pengguna bertanya yang berkaitan dengan resi.
        - status_order: jika pengguna bertanya yang berkaitan dengan status order.
        - price_list: jika pengguna bertanya tentang semua yang berkaitan dengan price list, harga atau yang serupa.
        - kanita: jika pengguna bertanya tentang diri kamu, identitas kamu, pencipta kamu, sumber data kamu.
        - unknown: jika pertanyaan tidak cocok dengan intent di atas.

        Balas hanya dengan satu kata intent dari daftar di atas, tanpa tambahan kata atau penjelasan. Jangan pernah membuat intent selain diatas.
    """

    full_prompt = prompt + "\nPertanyaan: " + question + "\nIntent:"

    try:
        ai_models = AIModels()
        intent = ai_models.generate_gemini_response(prompt=full_prompt)

        valid_intents = [
            "greetings",
            "thanks",
            "stok",
            "faq",
            "cek_resi",
            "status_order",
            "price_list",
            "kanita",
            "unknown",
        ]
        if intent in valid_intents:
            return intent
        else:
            return "unknown"

    except Exception as e:
        st.error(f"Error detecting intent: {e}")
        return "unknown"
