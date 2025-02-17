from helpers.get_time import get_time_of_day
from utils.get_memory import get_no_order


def prompt_generator(question: str, memory: any, intent: str, first: bool):
    time_of_day = get_time_of_day()
    no_order = get_no_order(question)
    intent_prompt = ""
    if intent == "a_greetings":
        intent_prompt = ""
    elif intent == "a_kanita":
        intent_prompt = ""
    elif intent == "a_notfound":
        intent_prompt = f"""Catatan: fitur cek resi itu adalah untuk mendapatkan nomor resi bukan untuk melacak. no order : {no_order}"""
    elif intent == "a_faq":
        intent_prompt = ""
    elif intent == "a_status_order":
        intent_prompt = f"""
          FORMAT:
            - Status Order "no_order" : status_order , buat lebih interaktif.
        """
    elif intent == "a_cek_resi":
        intent_prompt = f"""
          FORMAT:
            - Nomor Resi untuk "no_order" : no_resi , buat lebih interaktif.
        """
    elif intent == "a_stok":
        intent_prompt = f"""
          FORMAT:
          Jika terdapat lebih dari 1 jenis kain dan 1 cabang maka gunakan format berikut:
          - Lakukan group berdasarkan cabang
          1. kain - jenis warna - stok (Satuan)
          Jika terdapat 1 kain maka gunakan format berikut:
          - Lakukan group berdasarkan kain
          kain :
          1. jenis warna - stok (Satuan)
          Jika terdapat 1 cabang maka gunakan format berikut:
          kain :
          1. jenis warna - stok (Satuan)

          Penulisan stok untuk KG tulis menggunakan aslinya, untuk ROLL ditulis bulat misal 10 ROLL
        
          Untuk mendapatkan informasi lebih lengkap mengenai stok dapat dilihat melalui link berikut: https://stock.knitto.co.id
        """
    elif intent == "a_price_list":
        intent_prompt = f"""
          FORMAT:
            Pricelist cabang : 'cabang'.
            1. nama_kain - jenis_warna
            Harga Rollan :  'harga_rollan'.
            Harga >= 5 Kg : 'harga_diatas'.
            Harga < 5 Kg : 'harga_dibawah'.

            Buat lebih interaktif
        """
    else:
        intent_prompt = ""

    if first:
        greeting = f"Awali dengan kenalkan diri kamu sebagai Kanita yaitu Virtual Assistant Knitto Textile Indonesia, dan berikan salam sesuai wakut saat ini : {time_of_day}"
    else:
        greeting = ""

    prompt = f"""
        Jawablah pertanyaan berikut dengan konteks yang sudah diberikan, dan buat jawaban yang interaktif dengan mengembangkan konteks:

        Pertanyaan: "{question}"
        Konteks Jawaban: "{memory}"

        PERHATIAN:
        {intent_prompt}

        {greeting}

        Hindari :
        - Berdasarkan data kami, berdasarkan informasi yang kami miliki, atau berdasarkan informasi yang kami punya.
        - Gunakan bahasa yang ramah, profesional, dan langsung ke inti jawaban.
        - Jika tidak ada jawaban yang sesuai, beritahu saya untuk menganalisis kembali dan mencari jawaban yang lebih tepat.
        - Ketika menjawab gunakan emoji agar lebih interaktif dengan catatan tidak usah terlalu ramai.
        - Client = Kakak

        Lingkup:
        Jawaban yang diberikan hanya dilingkup hal-hal yang terkait dengan Knitto Textile Indonesia.
    """

    return prompt
