import google.generativeai as genai

def detect_intent(question):
    prompt = """
        Kamu adalah ahli bahasa yang bertugas mendeteksi intent dari pertanyaan pengguna dalam bahasa Indonesia.
        Intent yang tersedia adalah:
        - greetings: jika pengguna memberikan sapaan seperti "halo", "hi", atau sejenisnya.
        - thanks: jika pengguna mengucapkan terima kasih seperti "terima kasih", "makasih", atau sejenisnya.
        - stock_query: jika pengguna bertanya tentang stok kain atau atribut terkait, termasuk lokasi atau cabang.
        - profile: jika pengguna bertanya siapa kamu atau ingin mengetahui tentang Kanita.
        - introduce: jika pengguna bertanya untuk perkenalan diri atau bertanya tentang kamu, atau menanyakan siapa.
        - help_info: jika pengguna bertanya untuk informasi bantuan, bertanya tentang knitto, bertanya seputar cabang .
        - unknown: jika pertanyaan tidak cocok dengan intent di atas.

        Berikan hanya satu kata intent dari daftar di atas sebagai jawaban, tanpa penjelasan.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, question])
    return response.text.strip()
