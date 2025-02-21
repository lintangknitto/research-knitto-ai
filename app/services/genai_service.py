from utils.get_memory import get_memory_from_meili
from utils.intent_detection import detect_intent
from utils.prompt_generator import prompt_generator
from utils.mapping_memory import mapping_memory
from utils.augmented import generate_response


def summarize_memory(memory_data):
    summarized_memory = ""
    for entry in memory_data:
        summarized_memory += f"{entry['jawaban']} "
    return summarized_memory[:500]


def generate_answer_without_embed(
    question: str, first: bool, nohp: str, nama_customer: str
):
    if not nohp:
        prompt = prompt_generator(
            question,
            "Mohon masukkan nomor HP agar kami bisa memberikan informasi lebih lanjut.",
            "unauthorized",
            first,
        )
        try:
            return generate_response(model="gemini-2.0-flash", prompt=prompt, id='UNAUTHORIZED')
        except Exception as e:
            return f"Error 1: {e}"

    intent = detect_intent(question)
    print("Intent terdeteksi: ", intent)

    memory = get_memory_from_meili(intent, question, nohp)

    if (intent == "faq" or intent == "unknown") and len(memory) > 10:
        memory = summarize_memory(memory)

    intent_khusus = ["status_order", "stok", "cek_resi"]
    if not memory or (isinstance(memory, list) and len(memory) == 0):
        if intent in intent_khusus:
            memory = get_memory_from_meili("notfound", question, nohp=nohp, first_intent=intent)
        prompt = prompt_generator(
            question,
            memory,
            "notfound" if not memory else intent,
            first,
            nama_customer=nama_customer,
        )
    else:
        memory = mapping_memory(intent, memory)
        prompt = prompt_generator(
            question, memory, intent, first, nama_customer=nama_customer
        )

    
    try:
        response = generate_response(model="gemini-1.5-flash", prompt=prompt, id='GENERATE CHAT')
        print('CHAT', response)
        return response
    except Exception as e:
        return f"Error 2: {e}"
