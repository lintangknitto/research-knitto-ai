import meilisearch
from config.settings import MEILISEARCH_URL, MEILISEARCH_API_KEY
import re
from utils.spellchecker import correct_typo_with_rapidfuzz
from rapidfuzz import process
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from utils.preprocessing import preprocessing_text

stopword_factory = StopWordRemoverFactory()
stopwords_id = stopword_factory.get_stop_words()

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

client = meilisearch.Client(MEILISEARCH_URL, MEILISEARCH_API_KEY)


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


def get_kain(question: str):
    try:
        question = correct_typo_with_rapidfuzz(question)
        list_jenis_kain = ["combed 30s", "combed 20s", "combed 40s"]

        matches = process.extract(
            query=question, choices=list_jenis_kain, limit=5, score_cutoff=80
        )

        best_matches = [match[0] for match in matches]

        return best_matches if best_matches else []

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return []


def get_memory_from_meili(intent: str, question: str, nohp: str, first_intent=""):
    """Mengambil data dari MeiliSearch berdasarkan intent yang diberikan sebagai nama indeks."""

    intent_khusus = ["status_order", "stok", "cek_resi", "price_list"]
    try:
        if intent in intent_khusus:
            query = preprocessing_text(text=question, intent=intent)
        else:
            query = question
        filter_condition = ""
        print(f"Query yang diproses: {query}")

        index_selected = "faq"
        if intent == "greetings" or intent == "kanita":
            query = ""
            index_selected = intent
        elif intent == "notfound":
            no_order = get_no_order(query)
            query = ""
            index_selected = "notfound"

            if first_intent == "status_order":
                filter_condition = f"fitur = 'status_order'"
            elif first_intent == "a_cek_resi":
                filter_condition = f"fitur = 'cek_resi'"
            elif first_intent == "a_stok":
                filter_condition = f"fitur = 'cek_stok'"
        elif intent == "faq":
            index_selected = "faq"
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
        else:
            pass

        print("FILTER: ", filter_condition)
        index = client.index(index_selected)
        results = index.search(query, {"limit": 10, "filter": filter_condition})

        return results["hits"]

    except Exception as e:
        print(f"Error saat mengambil data dari MeiliSearch: {e}")
        return []
