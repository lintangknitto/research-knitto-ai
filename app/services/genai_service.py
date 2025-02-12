import google.generativeai as genai
from config.settings import GOOGLE_API_KEY
from helpers.get_time import get_time_of_day
from utils.memory import KANITA_MEMORY_JSON

# from utils.search_vector import retrieve_relevant_context
from utils.intent_detection import detect_intent

genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash")


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


def generate_answer_without_embed(question: str):
    """Menghasilkan jawaban berdasarkan memori (KANITA_MEMORY) dan intent pengguna."""
    time_of_day = get_time_of_day()

    intent = detect_intent(question)
    memory = KANITA_MEMORY_JSON[intent]
    print("Intent terdeteksi: ", intent)
    print("memory", memory)
    prompt = f"""
        Jawablah pertanyaan berikut dengan konteks yang sudah diberikan, dan buat jawaban yang interaktif dengan mengembangkan konteks:

        Pertanyaan: "{question}"
        Konteks Jawaban: "{memory}"

        Gunakan bahasa yang ramah dan profesional, dan pastikan lagi kalo kamu ini kanita jadi jawablah seperti profesional dalam pelayanan interaktif dan menjawab serta tidak terlalu kaku.

        PERHATIAN:
        - Hindari : Berdasarkan data kami, berdasarkan informasi yang kami miliki, atau berdasarkan informasi yang kami punya.
        - Jangan beritahu apakah kamu Kanita atau tidak, karena itu akan menambahkan kaku.
        - Jika tidak ada jawaban yang sesuai, beritahu saya untuk menganalisis kembali dan mencari jawaban yang lebih tepat.
    """

    try:
        response = MODEL.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        return f"Selamat {time_of_day}, terjadi kesalahan dalam menjawab pertanyaan Anda: {e}"
