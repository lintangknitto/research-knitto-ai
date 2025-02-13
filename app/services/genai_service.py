from config.model_client import MODEL
from helpers.get_time import get_time_of_day
from utils.get_memory import get_memory_from_meili

# from utils.search_vector import retrieve_relevant_context
from utils.intent_detection import detect_intent


# def generate_answer(question: str):
#     """Menghasilkan jawaban berdasarkan memori (EMBED)"""
#     time_of_day = get_time_of_day()

#     context = retrieve_relevant_context(question)
#     context_text = "\n".join(
#         [str(item) if isinstance(item, dict) else item for item in context]
#     )

#     print("question", question)
#     print("context", context)
#     print("text", context_text)
#     prompt = f"""
#         Kamu adalah Kanita, Virtual Assistant dari PT. Knitto Textile Indonesia. Jawabanmu harus ramah, profesional, dan interaktif.

#         Pertanyaan: "{question}"
#         Konteks Jawaban: "{context_text}"

#         Dari konteks yang diberikan susunlah dalam bahasa interaktif dan tidak mengikat pada konteks.

#         Gunakan bahasa yang ramah, profesional, dan langsung ke inti jawaban.
#         **Jangan gunakan frasa seperti "Berdasarkan informasi yang saya miliki" atau "Menurut data yang saya punya".**
#         Langsung jawab dengan jelas dan interaktif, seperti seorang master dalam pelayanan pelanggan.

#         Pastikan jawaban sesuai dengan peran Kanita sebagai asisten virtual PT. Knitto Textile Indonesia.
#     """

#     try:
#         response = MODEL.generate_content([prompt])
#         return response.text.strip()
#     except Exception as e:
#         return f"Selamat {time_of_day}, terjadi kesalahan dalam menjawab pertanyaan Anda: {e}"


def summarize_memory(memory_data):
    """Ringkas atau pilih bagian penting dari memory."""
    summarized_memory = ""
    for entry in memory_data:
        summarized_memory += f"{entry['jawaban']} "
    return summarized_memory[:500]


def generate_answer_without_embed(question: str, first: bool):
    """Menghasilkan jawaban berdasarkan memori (KANITA_MEMORY) dan intent pengguna."""
    time_of_day = get_time_of_day()
    print("first", first)

    intent = detect_intent(question)
    intent = "a_" + intent
    memory = get_memory_from_meili(intent, question)
    print("Intent terdeteksi: ", intent)
    print("memory sesuai intent", memory)

    intent_khusus = ["a_status_order", "a_cek_resi"]
    if not memory or (isinstance(memory, list) and len(memory) == 0):

        if intent in intent_khusus:
            memory = get_memory_from_meili("a_unknown", question)

        if not memory or (isinstance(memory, list) and len(memory) == 0):
            memory = get_memory_from_meili("a_faq", question)
            intent = "a_faq"
            print("memory_faq", memory)

    if intent == "a_faq" or intent == "a_unknown":
        memory = summarize_memory(memory)

    print("hasil memory", memory)

    if first:
        greeting = f"Awali dengan kenalkan diri kamu sebagai Kanita yaitu Virtual Assistant Knitto Textile Indonesia, dan berikan salam sesuai wakut saat ini : {time_of_day}"
    else:
        greeting = ""

    print(greeting)

    prompt = f"""
        Jawablah pertanyaan berikut dengan konteks yang sudah diberikan, dan buat jawaban yang interaktif dengan mengembangkan konteks:

        Pertanyaan: "{question}"
        Konteks Jawaban: "{memory}"

        Gunakan bahasa yang ramah dan profesional, dan pastikan lagi kalo kamu ini kanita jadi jawablah seperti profesional dalam pelayanan interaktif dan menjawab serta tidak terlalu kaku dan buat tidak terlalu formal.
        
        PERINTAH:
        {greeting}

        PERHATIAN:
        - Hindari : Berdasarkan data kami, berdasarkan informasi yang kami miliki, atau berdasarkan informasi yang kami punya.
        - Gunakan bahasa yang ramah, profesional, dan langsung ke inti jawaban.
        - Jika tidak ada jawaban yang sesuai, beritahu saya untuk menganalisis kembali dan mencari jawaban yang lebih tepat.
        - Ketika menjawab gunakan emoji agar lebih interaktif.
        - Client = Kakak
        
    """

    try:
        response = MODEL.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        return f"Terjadi kesalahan dalam proses jawaban: {e}"
