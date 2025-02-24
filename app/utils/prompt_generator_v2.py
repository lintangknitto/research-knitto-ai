from app.helpers.get_time import get_time_of_day
from app.utils.get_memory import get_no_order
from app.utils.get_memory import get_context
import json


INTENT_PROMPTS = {
    "notfound": r"""Buat penyampaian tentang tidak ditemukan dengan ramah.""",
    "status_order": r"""Jika terdapat list order pada context, gunakan format sebagai berikut. Jika pertanyaan seputar status order, untuk list > 1, **no ordernya** : **status ordernya**. Untuk list hanya 1, - No Order : **no_order** \n- Status Order: **status_order** \n- Tagihan: **tagihan** \n- Total Bayar: **total_bayar**. Jika pertanyaan seputar resi, untuk list > 1, **no ordernya** : **no resinya**. Untuk list hanya 1, - No Order : **no_order** \n- Status Order: **status_order** \n- Ongkir: **ongkir** \n- No Resi: **no_resi** \n- Ekspedisi: **ekspedisi**. Jika listnya > 1, tawarkan detailnya dengan minta nomer ordernya. Dan, apabila tidak terdapat list order, sampaikan kalo tidak ada order yang terdaftar dengan nomer telepon.""",
    "cek_resi": r"""Nomor Resi untuk "no_order" : **no_resi** , buat lebih interaktif.""",
    "stok": r"""Lakukan grouping berdasarkan cabang dan nama kain. Untuk pertanyaan yang cukup general atau tidak spesifik sampaikan untuk detailnya ada di link, dan sampaikan beberapa stok contoh sesuai yang ada di konteks. Penulisan stok untuk KG tulis menggunakan aslinya, untuk ROLL ditulis bulat misal 10 ROLL. Tidak usah tampilkan stok yang tidak sesuai pertanyaan. Untuk mendapatkan informasi lebih lengkap mengenai stok dapat dilihat melalui link berikut: https://stock.knitto.co.id""",
    "price_list": r"""Pricelist cabang : 'cabang'. 1. **nama_kain - jenis_warna** \n- Harga Rollan :  'harga_rollan' \n- Harga >= 5 Kg : 'harga_diatas' \n- Harga < 5 Kg : 'harga_dibawah' Apabila lebih dari 1 nama kain maka kelompokan dengan nama kain dan apabila terdapat warna yang harganya sama pada suatu nama kain maka gabungkan saja dalam list. Buat lebih interaktif, tapi tidak usah terlalu banyak emoji.""",
    "faq": r"""""",
}

MAIN_PROMPT_TEMPLATE = r"""Kamu adalah Kanita Virtual Assistant Knitto Textile Indonesia, yang merupakah Ahli Customer Service.
Tugas kamu adalah membantu user untuk menjawab pertanyaan. Gunakan bahasa yang ramah, profesional dan gunakan sedikit emoji untuk menunjukan perasaan.
Perlu kamu ketahui untuk menghindari jawaban dengan, frasa seperti 'berdasarkan data kamu' atau yang serupa, mengulangi pertanyaan, jawaban tidak relavan.
Selalu pastikan untuk menyebut user dengan "Kak". Buat agar user tidak merasa kaku. Ruang lingkup kamu hanya terkait dengan Knitto Textile Indonesia. Selalu minta customer bertanya kembali jika belum terima kasih.
Gunakan format berikut ini jika berkaitan dengan pertanyaan: {intent_prompt}
{greeting}
context:
{data_customer}
{context}
{informasi_cabang}
Berikut pertanyaan yang harus kamu jawab: {question}, jawab dengan baik dan jangan sampai context terbawa secara utuh
"""

MAIN_PROMPT_TEMPLATE_OPENAI = r"""Kamu adalah Kanita Virtual Assistant Knitto Textile Indonesia, yang merupakah Ahli Customer Service.
Tugas kamu adalah membantu user untuk menjawab pertanyaan. Gunakan bahasa yang ramah, profesional dan gunakan sedikit emoji untuk menunjukan perasaan.
Perlu kamu ketahui untuk menghindari jawaban dengan, frasa seperti 'berdasarkan data kamu' atau yang serupa, mengulangi pertanyaan, jawaban tidak relavan.
Selalu pastikan untuk menyebut user dengan "Kak". Buat agar user tidak merasa kaku. Ruang lingkup kamu hanya terkait dengan Knitto Textile Indonesia. Selalu minta customer bertanya kembali jika belum terima kasih.
Gunakan format berikut ini jika berkaitan dengan pertanyaan: {intent_prompt}
{greeting}
context:
{data_customer}
{context}
{informasi_cabang}
Berikut pertanyaan yang harus kamu jawab: {question}, jawab dengan baik dan jangan sampai context terbawa secara utuh
"""


def prompt_generator(
    question: str,
    intent: str,
    first_chat: bool,
    no_hp: str,
    first_intent: str,
    nama_customer="",
):
    try:
        time_of_day = get_time_of_day()
        no_order = get_no_order(question)
        greeting = (
            f"Awali dengan kenalkan diri kamu sebagai Kanita yaitu Virtual Assistant Knitto Textile Indonesia, dan berikan salam sesuai waktu saat ini : {time_of_day}"
            if first_chat
            else ""
        )

        data_cabang = ""
        if intent == "faq":
            data_cabang = get_context(intent="cabang", question="", nohp="")

        informasi_cabang = ""
        if data_cabang != "":
            informasi_cabang = (
                "Informasi cabang: "
                + data_cabang
                + ". Jika Customer berada tidak ada di cabang, sarankan cabang dengan alamat terdekat. Website: https://knitto.co.id. Customer portal untuk order online:https://portal.knitto.co.id"
            )

        if not no_hp:
            print("kadieee")
            prompt = MAIN_PROMPT_TEMPLATE.format(
                data_customer="",
                question=question,
                context="Minta customer untuk memasukan nomor hp. Karena customer belum memasukan nomor hp",
                intent_prompt="",
                greeting=greeting,
                informasi_cabang=informasi_cabang,
            )
            print(prompt)

            return prompt.strip()

        intent_prompt = INTENT_PROMPTS.get(intent, "").format(no_order=no_order)

        data_customer = (
            f"nama customer yang dilayani: {nama_customer}" if nama_customer else ""
        )

        context = get_context(
            intent=intent, question=question, nohp=no_hp, first_intent=first_intent
        )

        print("context", context)

        prompt = MAIN_PROMPT_TEMPLATE.format(
            data_customer=data_customer,
            question=question,
            context=context,
            intent_prompt=intent_prompt,
            greeting=greeting,
            informasi_cabang=informasi_cabang,
        )

        print("Generated Prompt:", prompt)
        result = {"prompt": prompt, "context": context}

        result_json = json.dumps(result, ensure_ascii=False)

        return result_json

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return "error"
    except Exception as e:
        print(f"Error in prompt_generator: {e}")
        return "error"
