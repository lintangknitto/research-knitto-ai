from helpers.get_time import get_time_of_day
from utils.get_memory import get_no_order
import tiktoken

INTENT_PROMPTS = {
    "notfound": r"""Fitur cek resi untuk nomor resi, bukan melacak. No order: {no_order}""",
    "status_order": r"""Format: Status Order "no_order": **status_order**. Jika tidak ada sampaikan kalo belum ada order. Selalu sebut order bukan pesanan""",
    "cek_resi": r"""Format: Nomor Resi untuk "no_order": no_resi.""",
    "stok": r"""Format: Grup berdasarkan cabang & nama kain. Stok KG: asli, ROLL: bulat (contoh: 10 ROLL). Stok kosong? Tanyakan kain lain. Info lengkap: https://stock.knitto.co.id. Untuk warna itu strict, jangan pernah menyamakan warna dari pertanyaan dengan warna dari konteks kecuali benar benar sama, jadi konteks tidak selalu sesuai maka harus pastikan lagi dan jika tidak ada yang sama sampaikan kalo tidak ada.""",
    "price_list": r"""Format: Pricelist cabang: 'cabang'. Nama kain - jenis warna: Harga Rollan, Harga >= 5 Kg, Harga < 5 Kg. Kelompokkan nama kain, gabungkan warna dengan harga sama. Buat interaktif.""",
}

FORMAT_DATA = {
    "stok": r"""Data berikut berisi informasi stok kain dalam format CSV: nama_kain,warna_kain,stok,satuan,cabang."""
}

MAIN_PROMPT_TEMPLATE = """
    Jawab pertanyaan berdasarkan konteks.

    {data_customer}

    Pertanyaan: "{question}"

    Konteks: "{memory}"

    Perhatian:
    {intent_prompt}
    {greeting}

    Saring data, jangan mengarang, tanyakan kembali.
    Gunakan bahasa yang relevan, emoji ramah.

    Lingkup:
    Knitto Textile Indonesia.
"""


def count_tokens(prompt: str):
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        token_integers = encoding.encode(prompt)
        num_tokens = len(token_integers)
        return num_tokens
    except Exception as e:
        print(f"Error encoding prompt: {e}")
        return -1


def prompt_generator(
    question: str, memory: any, intent: str, first: bool, nama_customer=""
):
    time_of_day = get_time_of_day()
    no_order = get_no_order(question)

    intent_prompt = INTENT_PROMPTS.get(intent, "").format(no_order=no_order)
    format_data = FORMAT_DATA.get(intent, "")

    greeting = f"Kanita (Virtual Assistant Knitto). {time_of_day}" if first else ""

    data_customer = f"Customer: Kak {nama_customer}" if nama_customer else ""

    prompt = MAIN_PROMPT_TEMPLATE.format(
        data_customer=data_customer,
        question=question,
        format_data=format_data,
        memory=memory,
        intent_prompt=intent_prompt,
        greeting=greeting,
    )

    return prompt.strip()
