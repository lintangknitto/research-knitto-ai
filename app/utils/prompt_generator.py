from helpers.get_time import get_time_of_day
from utils.get_memory import get_no_order
import tiktoken

INTENT_PROMPTS = {
    "notfound": r"""Buat penyampaian tentang tidak ditemukan dengan ramah.""",
    "status_order": r"""FORMAT: - Status Order "no_order" : **status_order** , tidak perlu memasukan tagihan atau lainya. Apabila pada pertanyaan ada spesifik no order maka pastikan yang ditampilkan sesuai no order yang diinginkan. Contoh MY140225001 dan OH140225001 itu berbeda. Tambahkan tagihan jika perlu dan ditanyakan. Ongkir jika perlu""",
    "cek_resi": r"""FORMAT: - Nomor Resi untuk "no_order" : **no_resi** , buat lebih interaktif.""",
    "stok": r"""FORMAT: Lakukan grouping berdasarkan cabang dan nama kain. Untuk pertanyaan yang cukup general atau tidak spesifik sampaikan untuk detailnya ada di link, dan sampaikan beberapa stok contoh sesuai yang ada di konteks. Penulisan stok untuk KG tulis menggunakan aslinya, untuk ROLL ditulis bulat misal 10 ROLL. Tidak usah tampilkan stok yang tidak sesuai pertanyaan. Untuk mendapatkan informasi lebih lengkap mengenai stok dapat dilihat melalui link berikut: https://stock.knitto.co.id""",
    "price_list": r"""FORMAT: Pricelist cabang : 'cabang'. 1. **nama_kain - jenis_warna** \n- Harga Rollan :  'harga_rollan' \n- Harga >= 5 Kg : 'harga_diatas' \n- Harga < 5 Kg : 'harga_dibawah' Apabila lebih dari 1 nama kain maka kelompokan dengan nama kain dan apabila terdapat warna yang harganya sama pada suatu nama kain maka gabungkan saja dalam list. Buat lebih interaktif, tapi tidak usah terlalu banyak emoji.""",
}

MAIN_PROMPT_TEMPLATE = r"""Jawablah pertanyaan berikut dengan konteks yang sudah diberikan, dan buat jawaban yang interaktif dengan mengembangkan konteks:
{data_customer}
**Pertanyaan:** "{question}"  
**Konteks Jawaban:** "{memory}"
### Perhatian:
{intent_prompt}
{greeting}
Saring data sesuai pertanyaan. Jika tidak ada data yang cocok, beri tahu tanpa mengarang.
### Hindari:
- Frasa seperti "berdasarkan data kami".
- Mengulangi pertanyaan.
- Jawaban tidak relevan.
- Gunakan bahasa ramah, sopan & profesional.
- Tambahkan emoji untuk interaksi.
- Selalu sebut customer sebagai "Kak" atau "Kakak".
- Buat agar customer tidak merasa kaku.
- "Berdasarkan informasi yang ada" atau yang serupa, ganti yang merujuk dengan saya siap menjawab apapun.
### Lingkup:
Kamu adalah kanita.
Jawaban hanya terkait dengan Knitto Textile Indonesia.
"""


def count_tokens(prompt: str):
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(prompt))
    except Exception as e:
        print(f"Error encoding prompt: {e}")
        return -1


def prompt_generator(
    question: str, memory: any, intent: str, first: bool, nama_customer=""
):
    try:
        time_of_day = get_time_of_day()
        no_order = get_no_order(question)
        intent_prompt = INTENT_PROMPTS.get(intent, "").format(no_order=no_order)

        greeting = (
            f"Awali dengan kenalkan diri kamu sebagai Kanita yaitu Virtual Assistant Knitto Textile Indonesia, dan berikan salam sesuai waktu saat ini : {time_of_day}"
            if first
            else ""
        )

        data_customer = (
            f"nama customer yang dilayani: {nama_customer}" if nama_customer else ""
        )

        prompt = MAIN_PROMPT_TEMPLATE.format(
            data_customer=data_customer,
            question=question,
            memory=memory,
            intent_prompt=intent_prompt,
            greeting=greeting,
        )
        
        print(prompt)
        return prompt.strip()

    except Exception as e:
        print(f"Error in prompt_generator: {e}")
        return "Mohon maaf, terjadi kesalahan dalam pembuatan jawaban. Silakan coba lagi nanti."
