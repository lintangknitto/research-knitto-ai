import meilisearch
from config.settings import MEILISEARCH_URL, MEILISEARCH_API_KEY
import re

client = meilisearch.Client(MEILISEARCH_URL, MEILISEARCH_API_KEY)

stopwords_id = [
    "yang",
    "dan",
    "di",
    "ke",
    "dari",
    "untuk",
    "dengan",
    "pada",
    "ini",
    "itu",
    "ada",
    "atau",
    "sebagai",
    "oleh",
    "bahwa",
    "saja",
    "untuk",
    "seperti",
    "lebih",
    "juga",
    "kami",
    "anda",
    "mereka",
    "kami",
    "tersebut",
    "atas",
    "adalah",
    "mengenai",
    "stok",
    "kain",
    "status",
    "order",
    "no order",
    "no",
    "cariin",
    "nomernya",
    "carikan",
    "resi",
]

tema_labels = {
    "aksesoris": "Aksesoris",
    "cacat_kain": "Cacat Kain",
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
}


def get_no_order(text):
    match = re.search(r"oh\d{9}", text)
    if match:
        return match.group()
    else:
        return ""


def preprocess_question(question: str) -> str:
    """Mempersiapkan pertanyaan agar lebih mudah dicari di MeiliSearch dalam bahasa Indonesia."""
    question = question.lower()
    question = re.sub(r"[^a-z0-9\s]", "", question)
    question = " ".join([word for word in question.split() if word not in stopwords_id])
    return question


def get_memory_from_meili(intent: str, question: str):
    """Mengambil data dari MeiliSearch berdasarkan intent yang diberikan sebagai nama indeks."""

    try:
        index = client.index(intent)
        query = preprocess_question(question)
        print(f"Query yang diproses: {query}")

        if intent == "a_greetings" or intent == 'a_kanita':
            query = ""

        if intent == "a_faq":
            filter_condition = ""
            for key, label in tema_labels.items():
                if key in query:
                    filter_condition = f"tema = '{label}'"
                    break
            if not filter_condition:
                filter_condition = f"tema = 'Umum'"

            print(filter_condition)
            results = index.search(query, {"filter": filter_condition})
        elif intent == "a_status_order" or intent == "a_cek_resi":
            no_order = get_no_order(query)
            filter_condition = f"no_order = '{no_order}' OR no_hp = '{query}'"

            print(filter_condition)
            results = index.search(query, {"filter": filter_condition})
        else:
            results = index.search(query)

        return results["hits"]

    except Exception as e:
        print(f"Error saat mengambil data dari MeiliSearch: {e}")
        return []
