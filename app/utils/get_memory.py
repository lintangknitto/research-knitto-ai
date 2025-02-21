import re
import time
from utils.preprocessing import preprocessing_text
from config.meilisearch_client import meiliClient

tema_labels = {
    "aksesoris": "Aksesoris",
    "cacat_kain": "Cacat Kain",
    "cara order": "Cara Order",
    "cara_order": "Cara Order",
    "complain": "Complain",
    "harga": "Harga",
    "hasil_kaos": "Hasil Kaos",
    "informasi_cabang": "Informasi Cabang",
    "jam_operasional": "Jam Operasional",
    "kain": "Kain",
    "kartu_nama": "Kartu Nama",
    "katalog": "Katalog",
    "konversi_ke_meter": "Konversi ke Meter",
    "lokasi": "Lokasi",
    "menunggu_pembayaran": "Menunggu Pembayaran",
    "minimal_pembelian": "Minimal Pembelian",
    "npwp": "NPWP",
    "pabrik": "Pabrik",
    "pajak": "Pajak",
    "pengiriman": "Pengiriman",
    "penjahit": "Penjahit",
    "perbedaan": "Perbedaan",
    "pre_order": "Pre Order",
    "print": "Print",
    "refund": "Refund",
    "rekomendasi": "Rekomendasi",
    "sablon_dtf": "Sablon DTF",
    "setrifikat": "Setrifikat",
    "status_order": "Status Order",
    "stock": "Stock",
    "susut": "Susut",
    "teknikal": "Teknikal",
    "telepon": "Telepon",
    "tentang_knitto": "Tentang Knitto",
    "warna": "Warna",
    "web_customer_portal_2": "Web Customer Portal 2",
    "fitur": "Fitur",
    "informasi": "Fitur",
}


def get_no_order(text):
    match = re.search(r"oh\d{9}", text)
    if match:
        return match.group()
    else:
        return ""


def get_no_hp(text):
    match = re.search(r"62\d{11}", text)
    if match:
        return match.group()
    else:
        return ""


def get_cabang(text):
    list_cabang = ["HOLIS", "KEBON JUKUT", "SUDIRMAN", "HOS COKROAMINOTO", "SOEKARNO"]

    for cabang in list_cabang:
        if re.search(r"\b" + re.escape(cabang) + r"\b", text, re.IGNORECASE):
            return cabang

    return ""


def get_memory_from_meili(intent: str, question: str, nohp: str, first_intent=""):
    """Mengambil data dari MeiliSearch berdasarkan intent yang diberikan sebagai nama indeks."""

    limit = 5
    intent_khusus = ["status_order", "stok", "cek_resi", "price_list"]
    try:
        if intent in intent_khusus:
            query = preprocessing_text(text=question, intent=intent)
        else:
            query = question
        filter_condition = ""
        print(f"Query yang diproses: {query}")

        index_selected = "unknown"
        if intent == "greetings" or intent == "kanita":
            query = ""
            index_selected = intent
        elif intent == "notfound":
            no_order = get_no_order(query)
            query = ""
            index_selected = "notfound"

            if first_intent == "status_order":
                filter_condition = f"fitur = 'status_order'"
            elif first_intent == "cek_resi":
                filter_condition = f"fitur = 'cek_resi'"
            elif first_intent == "stok":
                filter_condition = f"fitur = 'cek_stok'"
        elif intent == "faq":
            index_selected = "faq"
            limit = 2
            for key, label in tema_labels.items():
                if key in query:
                    filter_condition = f"tema = '{label}'"
                    break
        elif intent == "status_order" or intent == "cek_resi":
            no_order = get_no_order(query)
            if no_order:
                filter_condition = f"no_order = '{no_order}' AND no_hp = '{nohp}'"
            else:
                filter_condition = f"no_hp = '{nohp}'"
            query = ""
            index_selected = "status_order"
        elif intent == "stok" or intent == "price_list":
            cabang = get_cabang(question)
            conditions = []

            index_selected = "stok"
            if cabang:
                conditions.append(f"cabang = '{cabang}'")

            filter_condition = " AND ".join(conditions) if conditions else ""
        elif intent == 'cabang':
            index_selected = 'cabang'
            limit = 10
        else:
            pass

        index = meiliClient.index(index_selected)

        start_time = time.time()
        results = index.search(query, {"limit": limit, "filter": filter_condition})
        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        print("response time meilisearch: ", response_time, ' ms')

        return results["hits"]

    except Exception as e:
        print(f"Error saat mengambil data dari MeiliSearch: {e}")
        return []
