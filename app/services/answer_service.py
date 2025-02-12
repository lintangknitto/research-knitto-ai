from app.meilisearch import search_meilisearch
from app.filter import generate_filter
from app.generative import generate_content
from app.utils import get_time_of_day

def generate_answer(question, result):
    time_of_day = get_time_of_day()
    
    if not result:
        return f"Maaf, stok yang Anda cari tidak tersedia. Jika ada pertanyaan lain, jangan ragu untuk menghubungi saya. Terima kasih! 😊 Kanita"

    prompt_answer = f"""
        Kamu adalah Kanita, Virtual Assistant dari PT. Knitto Textile Indonesia. Tugas kamu adalah menjawab pertanyaan {question} dan susun jawabannya berdasarkan {result}.
        Jawaban harus profesional dan ramah, dengan fokus pada informasi produk dan stok.
        Gunakan informasi tentang waktu (seperti salam pagi, siang, sore) sesuai dengan waktu saat ini.
    """
    answer = generate_content(prompt_answer)
    return answer
