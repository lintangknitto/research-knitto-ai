from helpers.get_time import get_time_of_day
from utils.get_memory import get_no_order


def prompt_generator(question: str, memory: any, intent: str, first: bool, nama_customer = ""):
    time_of_day = get_time_of_day()
    no_order = get_no_order(question)
    intent_prompt = ""
    if intent == "greetings":
        intent_prompt = ""
    elif intent == "kanita":
        intent_prompt = ""
    elif intent == "notfound":
        intent_prompt = f"""Catatan: fitur cek resi itu adalah untuk mendapatkan nomor resi bukan untuk melacak. no order : {no_order}"""
    elif intent == "faq":
        intent_prompt = ""
    elif intent == "status_order":
        intent_prompt = f"""
          FORMAT:
            - Status Order "no_order" : **status_order** , tidak perlu memasukan tagihan atau lainya.
            
            Apabila pada pertanyaan ada spesifik no order maka pastikan yang ditampilkan sesuai no order yang diingikan. Contoh MY140225001 dan OH140225001 itu berbeda.
        """
    elif intent == "cek_resi":
        intent_prompt = f"""
          FORMAT:
            - Nomor Resi untuk "no_order" : no_resi , buat lebih interaktif.
        """
    elif intent == "stok":
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

          Penulisan stok untuk KG tulis menggunakan aslinya, untuk ROLL ditulis bulat misal 10 ROLL.
          
          Note: Maaf, stok yang Anda cari saat ini kosong atau tidak tersedia.
        
          Untuk mendapatkan informasi lebih lengkap mengenai stok dapat dilihat melalui link berikut: https://stock.knitto.co.id
        """
    elif intent == "price_list":
        intent_prompt = f"""
          FORMAT:
            Pricelist cabang : 'cabang'.
            1. **nama_kain - jenis_warna**
            Harga Rollan :  'harga_rollan'.
            Harga >= 5 Kg : 'harga_diatas'.
            Harga < 5 Kg : 'harga_dibawah'.

            Apabila lebih dari 1 nama kain maka kelompokan dengan nama kain.
            Buat lebih interaktif, tapi tidak usah terlalu banyak emoji.
        """
    else:
        intent_prompt = ""

    if first:
        greeting = f"Awali dengan kenalkan diri kamu sebagai Kanita yaitu Virtual Assistant Knitto Textile Indonesia, dan berikan salam sesuai wakut saat ini : {time_of_day}"
    else:
        greeting = ""
    
    if nama_customer:
        data_customer = f"""nama customer yang dilayani: {nama_customer}"""
    else:
        data_customer = ""

    prompt = f"""
        Jawablah pertanyaan berikut dengan konteks yang sudah diberikan, dan buat jawaban yang interaktif dengan mengembangkan konteks:

        {data_customer}
        
        Pertanyaan: "{question}"
        Konteks Jawaban: "{memory}"

        PERHATIAN:
        {intent_prompt}

        {greeting}

        Hindari :
        - Berdasarkan data kami, berdasarkan informasi yang kami miliki, atau berdasarkan informasi yang kami punya.
        - Jangan mengulangi pertanyaan.
        - Jangan pernah mengarang jawaban apabila konteks tidak ada.
        - Gunakan bahasa yang ramah, profesional, dan langsung ke inti jawaban.
        - Jika tidak ada jawaban yang sesuai, beritahu saya untuk menganalisis kembali dan mencari jawaban yang lebih tepat.
        - Ketika menjawab gunakan emoji agar lebih interaktif dengan catatan tidak usah terlalu ramai.
        - Client = Kakak

        Lingkup:
        Jawaban yang diberikan hanya dilingkup hal-hal yang terkait dengan Knitto Textile Indonesia.
    """

    return prompt
