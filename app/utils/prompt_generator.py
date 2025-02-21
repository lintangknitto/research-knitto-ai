from helpers.get_time import get_time_of_day
from utils.get_memory import get_no_order
from utils.get_memory import get_memory_from_meili
from utils.mapping_memory import mapping_memory

INTENT_PROMPTS = {
    "notfound": r"""Buat penyampaian tentang tidak ditemukan dengan ramah.""",
    "status_order": r""""no_order" : **status_order** , tidak perlu memasukan tagihan atau lainya. Apabila pada pertanyaan ada spesifik no order maka pastikan yang ditampilkan sesuai no order yang diinginkan. Contoh MY140225001 dan OH140225001 itu berbeda. Tambahkan tagihan jika perlu dan ditanyakan. Ongkir jika perlu""",
    "cek_resi": r"""Nomor Resi untuk "no_order" : **no_resi** , buat lebih interaktif.""",
    "stok": r"""Lakukan grouping berdasarkan cabang dan nama kain. Untuk pertanyaan yang cukup general atau tidak spesifik sampaikan untuk detailnya ada di link, dan sampaikan beberapa stok contoh sesuai yang ada di konteks. Penulisan stok untuk KG tulis menggunakan aslinya, untuk ROLL ditulis bulat misal 10 ROLL. Tidak usah tampilkan stok yang tidak sesuai pertanyaan. Untuk mendapatkan informasi lebih lengkap mengenai stok dapat dilihat melalui link berikut: https://stock.knitto.co.id""",
    "price_list": r"""Pricelist cabang : 'cabang'. 1. **nama_kain - jenis_warna** \n- Harga Rollan :  'harga_rollan' \n- Harga >= 5 Kg : 'harga_diatas' \n- Harga < 5 Kg : 'harga_dibawah' Apabila lebih dari 1 nama kain maka kelompokan dengan nama kain dan apabila terdapat warna yang harganya sama pada suatu nama kain maka gabungkan saja dalam list. Buat lebih interaktif, tapi tidak usah terlalu banyak emoji.""",
    "faq": r""""""
}

MAIN_PROMPT_TEMPLATE = r"""Kamu adalah Kanita Virtual Assistant Knitto Textile Indonesia, yang merupakah Ahli Customer Service.
Tugas kamu adalah membantu user untuk menjawab pertanyaan. Gunakan bahasa yang ramah, profesional dan gunakan sedikit emoji untuk menunjukan perasaan.
Perlu kamu ketahui untuk menghindari jawaban dengan, frasa seperti 'berdasarkan data kamu' atau yang serupa, mengulangi pertanyaan, jawaban tidak relavan.
Selalu pastikan untuk menyebut user dengan "Kak". Buat agar user tidak merasa kaku. Ruang lingkup kamu hanya terkait dengan Knitto Textile Indonesia. Selalu minta customer bertanya kembali jika belum terima kasih.
{greeting}
{data_customer}
{memory}
{informasi_cabang}
Berikut pertanyaan yang harus kamu jawab: {question}
Gunakan format berikut ini jika berkaitan dengan pertanyaan: {intent_prompt}
"""

def prompt_generator(
    question: str, memory: any, intent: str, first: bool, nama_customer=""
):
    try:
        time_of_day = get_time_of_day()
        no_order = get_no_order(question)
        data_cabang = get_memory_from_meili(intent='cabang', question='', nohp='')

        informasi_cabang = ""
        if not data_cabang:
            data_cabang = ""
        else:
            data_cabang = mapping_memory(intent='cabang', data=data_cabang)
            
        print(data_cabang)
        
        informasi_cabang = "Informasi cabang" +  data_cabang + '. Jika Customer berada tidak ada di cabang, sarankan cabang dengan alamat terdekat'
        
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
            informasi_cabang=informasi_cabang
        )
        
        print('Generated Prompt:', prompt)

        return prompt.strip()

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return 'error'
    except Exception as e:
        print(f"Error in prompt_generator: {e}")
        return 'error'

