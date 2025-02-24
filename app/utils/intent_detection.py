from utils.augmented import generate_response
import streamlit as st


def detect_intent(question: str):
    prompt = f"""Kamu adalah Intent Detection Expert. Tugas kamu adalah mendeteksi intent dari setiap pertanyaan atau kalimat yang dimasukan oleh user. Dalam mendeteksi intent, scope yang kamu miliki adalah sebagai berikut: greetings, thanks, stok, faq, status_order(tagihan, ongkir, ekspedisi), price_list, kanita, faq. Untuk pertanyaan yang hanya mengandung nomor order masukan sebagai status_order. Jika menurut kamu kalimat yang diberikan tidak masuk kedalam scope diatas, maka bisa dimasukan saja sebagai faq. Berikut kalimat yang harus dideteksi : {question}. Jawab hanya intentnya saja, misalnya "stok". Dan jangan dijawab selain scope yang sudah disebutkan.
    """
    
    try:
        intent = generate_response(model="gemini-2.0-flash", prompt=prompt, id='INTENT DETECTION')

        valid_intents = [
            "greetings",
            "thanks",
            "stok",
            "faq",
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
