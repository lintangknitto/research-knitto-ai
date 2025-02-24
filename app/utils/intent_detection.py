from app.utils.augmented import generate_response
import json


def detect_intent(question: str):
    prompt = f"""Kamu adalah Intent Detection Expert. Tugas kamu adalah mendeteksi intent dari setiap pertanyaan atau kalimat yang dimasukan oleh user. Dalam mendeteksi intent, scope yang kamu miliki adalah sebagai berikut: greetings, thanks, stok, faq, status_order(tagihan, ongkir, ekspedisi), price_list, kanita, faq. Untuk pertanyaan yang hanya mengandung nomor order masukan sebagai status_order. Jika menurut kamu kalimat yang diberikan tidak masuk kedalam scope diatas, maka bisa dimasukan saja sebagai faq. Berikut kalimat yang harus dideteksi : {question}. Jawab hanya intentnya saja, misalnya "stok". Dan jangan dijawab selain scope yang sudah disebutkan.
    """

    try:
        response = generate_response(
            model="gemini-1.5-flash", prompt=prompt, id="INTENT DETECTION"
        )

        response_json = json.loads(response)

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

        if response_json.get("response_content") in valid_intents:
            return response_json.get("response_content")
        else:
            return "unknown"
    except Exception as e:
        return "unknown"
