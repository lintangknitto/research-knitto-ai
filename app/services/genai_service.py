from config.model_client import AIModels
from utils.get_memory import get_memory_from_meili
from utils.intent_detection import detect_intent
from utils.prompt_generator import prompt_generator
from utils.spellchecker import correct_typo_with_rapidfuzz


def summarize_memory(memory_data):
    """Ringkas atau pilih bagian penting dari memory."""
    summarized_memory = ""
    for entry in memory_data:
        summarized_memory += f"{entry['jawaban']} "
    return summarized_memory[:500]


def generate_answer_without_embed(question: str, first: bool):
    """Menghasilkan jawaban berdasarkan memori (KANITA_MEMORY) dan intent pengguna."""
    print("first", first)
    question = correct_typo_with_rapidfuzz(question)
    intent = detect_intent(question)
    intent = "a_" + intent
    memory = get_memory_from_meili(intent, question)
    print("Intent terdeteksi: ", intent)
    intent_khusus = ["a_status_order", "a_cek_resi", "a_stok"]
    first_intent = intent

    if (intent == "a_faq" or intent == "a_unknown") and len(memory) > 10:
        memory = summarize_memory(memory)

    print("memory", memory)
    prompt = prompt_generator(question, memory, intent, first)

    if not memory or (isinstance(memory, list) and len(memory) == 0):
        if intent in intent_khusus:
            print("NOTFOUND")
            memory = get_memory_from_meili("a_notfound", question, first_intent)
            prompt = prompt_generator(question, memory, "a_notfound", first)

    try:
        ai_model = AIModels()
        return ai_model.generate_response(model="gemini-1.5-flash", prompt=prompt)
    except Exception as e:
        return f"Terjadi kesalahan dalam proses jawaban: {e}"
