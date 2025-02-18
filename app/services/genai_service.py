from config.model_client import AIModels
from utils.get_memory import get_memory_from_meili
from utils.intent_detection import detect_intent
from utils.prompt_generator import prompt_generator
from utils.spellchecker import correct_typo_with_rapidfuzz
from utils.preprocessing import preprocessing_text


def summarize_memory(memory_data):
    """Ringkas atau pilih bagian penting dari memory."""
    summarized_memory = ""
    for entry in memory_data:
        summarized_memory += f"{entry['jawaban']} "
    return summarized_memory[:500]


def generate_answer_without_embed(
    question: str, first: bool, nohp: str, nama_customer: str
):
    """Menghasilkan jawaban berdasarkan memori (KANITA_MEMORY) dan intent pengguna."""
    if nohp:
        intent = detect_intent(question)
        memory = get_memory_from_meili(intent, question, nohp)
        print("Intent terdeteksi: ", intent)

        text_pre = preprocessing_text(text=question, intent=intent)

        print("TEXTPREEE", text_pre)
        if (intent == "faq" or intent == "unknown") and len(memory) > 10:
            memory = summarize_memory(memory)

        prompt = prompt_generator(
            question, memory, intent, first, nama_customer=nama_customer
        )

        intent_khusus = ["a_status_order", "a_cek_resi", "a_stok"]
        first_intent = intent
        if not memory or (isinstance(memory, list) and len(memory) == 0):
            if intent in intent_khusus:
                memory = get_memory_from_meili(
                    "notfound", question, first_intent, nohp=nohp
                )
                prompt = prompt_generator(
                    question, memory, "notfound", first, nama_customer=nama_customer
                )
    else:
        prompt = prompt_generator(
            question,
            "nomor hp perlu dimasukan, buat lebih interaktif. Tanpa nomer hp tidak bisa memberikan informasi lebih jauh",
            "unauthorized",
            first,
        )

    try:
        ai_model = AIModels()
        return ai_model.generate_response(model="gemini-1.0-pro", prompt=prompt)
    except Exception as e:
        return f"Terjadi kesalahan dalam proses jawaban: {e}"
