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
        return f"Error generating filter: {e}"
