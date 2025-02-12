import streamlit as st
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MEILISEARCH_URL = os.getenv("MEILISEARCH_URL")
MEILISEARCH_API_KEY = os.getenv("MEILISEARCH_API_KEY")
INDEX_NAME = "data_stok"

headers = {
    "Authorization": f"Bearer {MEILISEARCH_API_KEY}",
    "Content-Type": "application/json"
}

def search_meilisearch(query_filter):
    try:
        url = f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/search"
        payload = {
            "q": "",
            "filter": query_filter
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("hits", [])
    except requests.RequestException as e:
        st.error(f"Error querying MeiliSearch: {e}")
        return []

def get_time_of_day():
    indonesian_tz = pytz.timezone("Asia/Jakarta")
    
    now = datetime.now(indonesian_tz)
    
    if 5 <= now.hour < 10:
        return "pagi"
    elif 10 <= now.hour < 15:
        return "siang"
    elif 15 <= now.hour < 18:
        return "sore"
    else:
        return "malam"

def generate_filter(question: str):
    prompt = """
        Kamu adalah ahli dalam mengubah pertanyaan dalam bahasa Indonesia menjadi filter untuk MeiliSearch.
        Index bernama `data_stok` dengan atribut seperti `nama_kain`, `jenis_warna`,`cabang`, `stok_terberat`, dan `jmlstok`(roll). Dan cabang yang tersedia itu ada 'HOLIS', 'HOS COKROAMINOTO', 'KEBON JUKUT', 'SOEKARNO' ,'SUDIRMAN', 'SEMARANG'.
        
        INSTRUKSI:
        - Jika pertanyaan berupa sapaan dan tidak mengandung pertanyaan tentang stok atau kata kata stok.
        - Filter harus berupa string logika dalam format:
          nama_kain = '{nama_kain}' AND jenis_warna = '{jenis_warna}' AND cabang = '{cabang}'
          tapi jika tidak menyebutkan spesifik cabang maka tidak usah menyertakan cabang.
        - Kecualikan kain dengan nama `RIB`, `KRAH`, dan `Manset`. dengan cara nama_kain NOT CONTAINS
        - Jangan tambahkan informasi lain selain format yang diminta.
        - Jangan menyertakan atribut yang tidak relevan atau kosong.
        - Jika menanyakan terbanyak atau tertinggi maka filter dari jmlstok yang terbanyak.
        Hasil akhirnya harus berupa string filter.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, question])
        cleaned_response = response.text.replace('```', '').strip()
        
        if cleaned_response.lower() == "greetings":
            return "greetings"
        
        return cleaned_response
    except Exception as e:
        st.error(f"Error generating filter: {e}")
        return None

KANITA_MEMORY = {
    "profile": "Saya adalah asisten virtual yang membantu menjawab pertanyaan terkait produk kain, stok kain, warna, serta informasi tentang cabang-cabang PT. Knitto Textile Indonesia.",
    "introduction": "Halo! Saya **Kanita**, Virtual Assistant dari PT. Knitto Textile Indonesia. 😊 Saya bisa membantu Anda dengan berbagai hal terkait produk kain, stok kain, warna, dan cabang kami.",
    "role": "Saya adalah asisten virtual yang membantu menjawab pertanyaan terkait produk kain, stok, warna, serta informasi tentang cabang-cabang PT. Knitto Textile Indonesia.",
    "help_info": {
        "general": [
            "Menyediakan informasi **stok kain** yang tersedia di cabang-cabang kami.",
            "Memberikan detail tentang **jenis kain** dan **warna** yang tersedia.",
            "Menyediakan informasi terkait **lokasi cabang** kami (seperti HOLIS, KEBON JUKUT, SOEKARNO, dll).",
            "Jika Anda membutuhkan bantuan lebih lanjut, jangan ragu untuk bertanya!"
        ],
        "cabang": [
            {
                "name": "HOLIS",
                "lokasi": "Bandung"
            },
            {
                "name": "HOS COKROAMINOTO",
                "lokasi": "Jogja"
            },
            {
                "name": "KEBON JUKUT",
                "lokasi": "Bandung"
            },
            {
                "name": "SOEKARNO",
                "lokasi": "Surabaya"
            },
            {
                "name": "SUDIRMAN",
                "lokasi": "Semarang"
            }
        ],
        "additional": [
            "Menampilkan tentang data atau sejarah"
        ]
    },
    "greetings": [
        "Halo! Saya Kanita, Virtual Assistant dari PT. Knitto Textile Indonesia. 😊 Ada yang bisa saya bantu?"
    ],
    "thanks": [
        "Sama-sama! Jika ada pertanyaan lain, jangan ragu untuk menghubungi saya. 😊 Kanita"
    ],
    "unknown": [
        "Mohon maaf saya tidak mengerti pertanyaan anda"
    ]
}

def detect_intent(question: str):
    prompt_intent = """
        Kamu adalah ahli bahasa yang bertugas mendeteksi intent dari pertanyaan pengguna dalam bahasa Indonesia.
        Intent yang tersedia adalah:
        - greetings: jika pengguna memberikan sapaan seperti "halo", "hi", atau sejenisnya ataupun mengenalkan dirinya.
        - thanks: jika pengguna mengucapkan terima kasih seperti "terima kasih", "makasih", atau sejenisnya.
        - stock_query: jika pengguna bertanya tentang stok kain atau atribut terkait, termasuk lokasi atau cabang.
        - profile: jika pengguna bertanya siapa kamu atau ingin mengetahui tentang Kanita.
        - introduction: jika pengguna bertanya untuk perkenalan diri atau bertanya tentang kamu, atau menanyakan siapa.
        - help_info: jika pengguna bertanya untuk informasi bantuan, bertanya tentang knitto, bertanya seputar cabang .
        - unknown: jika pertanyaan tidak cocok dengan intent di atas.

        Berikan hanya satu kata intent dari daftar di atas sebagai jawaban, tanpa penjelasan.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt_intent, question])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error detecting intent: {e}")
        return "unknown"

def generate_answer(question: str, result):
    time_of_day = get_time_of_day()

    prompt_answer = f"""
        Kamu adalah Kanita, Virtual Assistant dari PT. Knitto Textile Indonesia. Tugas kamu adalah menjawab {question} dan susun jawabannya dari {result}. Kamu adalah asisten yang ramah, profesional, dan informatif. Jawabanmu harus relevan, detail, dan fokus hanya pada topik terkait PT. Knitto Textile Indonesia, termasuk produk kain, stok, layanan, atau hal lain yang berkaitan.

        Panduan:
        - Jika jmlstok > 0 maka stok = jmlstok dengan satuan Roll. Selain itu maka stok = stok_terberat satuan Kg.
    
        Instruksi:
        - Jawaban harus singkat, ramah, dan langsung memberikan informasi yang relevan sesuai pertanyaan pengguna.
        - Jika tidak ada data yang tersedia, berikan jawaban sopan tanpa menyalahkan pengguna.
        - Format jawaban untuk stok: "Kain - Warna : Stok".
        - Akhiri dengan kalimat: “Jika ada pertanyaan lain, jangan ragu untuk menghubungi saya. Terima kasih! 😊 Kanita”.
        - Sesuaikan bahasa jawaban dengan bahasa pertanyaan.
        - Menggunakan salam yang sesuai dengan waktu, seperti: "Selamat {time_of_day}". Dan kalo di pertanyaan waktunya tidak sesuai koreksi saja dengan sopan dan ramah.
    """
    try:
        result_str = str(result)
        if not result_str or result_str == "[]": 
            return f"Mohon maaf, stok yang Anda cari tidak tersedia. Jika ada pertanyaan lain, jangan ragu untuk menghubungi saya. Terima kasih! 😊 Kanita"
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt_answer])
        return response.text.strip()
    except Exception as e:
        print(e)
        st.error(f"Error generating answer: {e}")
        return "Mohon maaf, terjadi kesalahan dalam menyusun jawaban. Jika ada pertanyaan lain, jangan ragu untuk menghubungi saya. 😊 Kanita"


def get_knowledge(question):
    prompt = f"""
        {question}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error get knowledge: {e}")
        return ''

def generate_memory_based_answer(question):
    time_of_day = get_time_of_day()
    intent = detect_intent(question)
    print(intent)
    
    if intent == 'stock_query':
        query_filter = generate_filter(question)
        if query_filter:
            result = search_meilisearch(query_filter)
            answer = generate_answer(question, result)
        else:
            answer = "Maaf, saya tidak dapat memahami pertanyaan Anda terkait stok."
        
        return answer
    
    prompt = f"""
        Kamu adalah Kanita, Virtual Assistant dari PT. Knitto Textile Indonesia. Jawabanmu harus ramah, profesional, dan interaktif.
        Berikut adalah konteks tentang kamu:
        {KANITA_MEMORY[intent]}

        Gunakan konteks ini untuk menjawab pertanyaan berikut secara ramah dan interaktif:
        "{question}"

        Pastikan jawabanmu:
        - Interaktif dan menyertakan sapaan.
        - Memberikan informasi sesuai konteks memori.
        - Mengajak pengguna untuk bertanya lebih lanjut.
        - Selalu hangat dan menjawab sapaan sesuai waktu, seperti "Selamat {time_of_day}".
        
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating memory-based answer: {e}")
        return KANITA_MEMORY[memory_key]

def main():
    st.title("Kanita Chatbot - PT. Knitto Textile Indonesia")
    st.subheader("Virtual Assistant")

    question = st.text_input("Masukkan pertanyaan Anda:")

    if question:
        answer = generate_memory_based_answer(question)

        st.write("Jawaban dari Kanita:")
        st.success(answer)

if __name__ == "__main__":
    main()

