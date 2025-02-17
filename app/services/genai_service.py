from config.model_client import MODEL, MODEL_OPEN_AI
from helpers.get_time import get_time_of_day
from utils.get_memory import get_memory_from_meili
from utils.intent_detection import detect_intent


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
            memory = get_memory_from_meili("a_notfound", question)

    if (intent == "a_faq" or intent == "a_unknown") and len(memory) > 10:
        memory = summarize_memory(memory)

    if intent == "a_stok":
        additional = "Untuk mendapatkan informasi lebih lengkap mengenai stok dapat dilihat melalui link berikut: https://stock.knitto.co.id"
    else:
        additional = ""

    if first:
        greeting = f"Awali dengan kenalkan diri kamu sebagai Kanita yaitu Virtual Assistant Knitto Textile Indonesia, dan berikan salam sesuai wakut saat ini : {time_of_day}"
    else:
        greeting = ""

    print("memory", memory)

    prompt = f"""
        Jawablah pertanyaan berikut dengan konteks yang sudah diberikan, dan buat jawaban yang interaktif dengan mengembangkan konteks:

        Konteks Jawaban: "{memory}"

        Gunakan bahasa yang ramah dan profesional, dan pastikan lagi kalo kamu ini kanita jadi jawablah seperti profesional dalam pelayanan interaktif dan menjawab serta tidak terlalu kaku dan buat tidak terlalu formal.
        
        PERINTAH:
        {greeting}
        
        ADDITIONAL:
        {additional}

        PERHATIAN:
        - Hindari : Berdasarkan data kami, berdasarkan informasi yang kami miliki, atau berdasarkan informasi yang kami punya.
        - Gunakan bahasa yang ramah, profesional, dan langsung ke inti jawaban.
        - Jika tidak ada jawaban yang sesuai, beritahu saya untuk menganalisis kembali dan mencari jawaban yang lebih tepat.
        - Ketika menjawab gunakan emoji agar lebih interaktif dengan catatan tidak usah terlalu ramai.
        - Client = Kakak
        
        Lingkup:
        - Jawaban yang diberikan hanya dilingkup hal hal yang terkait dengan knitto textile indonesia
    """

    try:
        # response = MODEL.generate_content([prompt])
        # return response.text.strip()
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ]
        
        print(messages)

        response = MODEL_OPEN_AI.completions.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo model
            messages=messages,  # The conversation context
            max_tokens=800,  # Limit the length of the response
        )
        
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Terjadi kesalahan dalam proses jawaban: {e}"
