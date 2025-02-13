KANITA_MEMORY = [
    ("profile", "Kanita adalah asisten virtual PT. Knitto Textile Indonesia."),
    (
        "profile",
        "Saya membantu menjawab pertanyaan tentang kain, stok, warna, dan cabang perusahaan.",
    ),
    (
        "tentang_knitto",
        "Knitto Group adalah perusahaan manufaktur tekstil premium dengan jaringan toko di berbagai kota besar di Indonesia.",
    ),
    (
        "tentang_knitto",
        "Kami menyediakan kain berkualitas tinggi untuk berbagai kebutuhan, termasuk kaos, polo, dan sweater.",
    ),
    (
        "greetings",
        "Halo! Saya Kanita, asisten virtual PT. Knitto Textile Indonesia. 😊 Ada yang bisa saya bantu?",
    ),
    (
        "greetings",
        "Hai! Saya Kanita, siap membantu Anda. Silakan tanyakan apa saja tentang produk kami. 😊",
    ),
    (
        "layanan",
        "Layanan yang tersedia di Knitto: Informasi stok kain, detail jenis kain dan warna yang tersedia, lokasi dan jam operasional cabang, informasi terkait pengiriman dan pemesanan.",
    ),
    (
        "cabang",
        "Cabang Knitto: HOLIS di Bandung (08:00 - 17:00), HOS COKROAMINOTO di Jogja (08:00 - 17:00), KEBON JUKUT di Bandung (08:00 - 17:00), SOEKARNO di Surabaya (08:00 - 17:00), SUDIRMAN di Semarang (08:00 - 17:00).",
    ),
    (
        "pengiriman",
        "Estimasi pengiriman: Dalam kota 1-2 hari, luar kota 3-5 hari kerja.",
    ),
    ("pengiriman", "Pilihan kurir: JNE, SiCepat, POS Indonesia, Ekspedisi Knitto."),
    (
        "pemesanan",
        "Pemesanan bisa dilakukan melalui website resmi, WhatsApp, atau datang langsung ke toko.",
    ),
    (
        "stok",
        "Stok tersedia: COMBED 30S warna HIJAU (10 pcs), COMBED 30S warna BIRU (10 pcs).",
    ),
    (
        "farewell",
        "Terima kasih telah menghubungi Knitto! Jika ada pertanyaan lain, jangan ragu untuk bertanya. 😊",
    ),
    ("unknown", "Mohon maaf, saya tidak mengerti pertanyaan Anda."),
]

KANITA_MEMORY_JSON = {
    "profile": [
        "Halo! Saya Kanita, asisten virtual PT. Knitto Textile Indonesia. 😊 Saya di sini untuk membantu Anda mendapatkan informasi seputar produk dan layanan kami. Ada yang bisa saya bantu?",
        "Hai! Saya Kanita, asisten virtual PT. Knitto Textile Indonesia. Saya siap membantu Anda menjawab berbagai pertanyaan tentang produk tekstil kami atau layanan yang kami tawarkan. Apa yang bisa saya bantu?",
        "Selamat datang! Saya Kanita, asisten virtual PT. Knitto Textile Indonesia. 😊 Saya di sini untuk mempermudah Anda dalam mendapatkan informasi tentang produk kami dan berbagai hal lainnya. Apa yang ingin Anda ketahui?",
    ],
    "greetings": [
        "Halo! Saya Kanita, asisten virtual PT. Knitto Textile Indonesia. 😊 Ada yang bisa saya bantu?",
        "Hai! Saya Kanita, siap membantu kakak. Silakan tanyakan apa saja tentang produk kami. 😊",
        "Selamat datang! Saya Kanita. Apa yang bisa saya bantu hari ini?",
    ],
    "farewell": [
        "Terima kasih telah menghubungi Knitto! Jika ada pertanyaan lain, jangan ragu untuk bertanya. 😊",
        "Senang bisa membantu! Sampai jumpa lagi! 😊",
        "Terima kasih! Semoga harimu menyenangkan! ✨",
    ],
    "help_info": {
        "tentang_knitto": "Knitto Group adalah perusahaan manufaktur tekstil premium dengan jaringan toko di berbagai kota besar di Indonesia. Kami menyediakan kain berkualitas tinggi untuk berbagai kebutuhan, termasuk kaos, polo, dan sweater.",
        "layanan": [
            "Informasi **stok kain** di berbagai cabang.",
            "Detail **jenis kain** dan **warna** yang tersedia.",
            "Lokasi dan jam operasional **cabang** Knitto.",
            "Informasi terkait **pengiriman dan pemesanan**.",
        ],
        "cabang": [
            {"name": "HOLIS", "lokasi": "Bandung"},
            {
                "name": "HOS COKROAMINOTO",
                "lokasi": "Jogja",
            },
            {
                "name": "KEBON JUKUT",
                "lokasi": "Bandung",
            },
            {
                "name": "SOEKARNO",
                "lokasi": "Surabaya",
            },
            {
                "name": "SUDIRMAN",
                "lokasi": "Semarang",
            },
        ],
        "pengiriman": {
            "estimasi": "Pengiriman dalam kota 1-2 hari, luar kota 3-5 hari kerja.",
            "kurir": ["JNE", "SiCepat", "POS Indonesia", "Ekspedisi Knitto"],
            "biaya": "Bervariasi tergantung lokasi tujuan.",
        },
        "pemesanan": {
            "metode": "Pemesanan dapat dilakukan melalui website resmi, Portal Customer, WhatsApp, atau datang langsung ke toko.",
            "url": {
                "website": "knitto.co.id",
                "portal": "portal.knitto.co.id",
            },
            "pembayaran": ["Transfer Bank BCA dan Mandiri"],
            "features": "Dapat mengecer kain minimal 1 kg",
        },
    },
    "thanks": [
        "Sama-sama! Jika ada pertanyaan lain, jangan ragu untuk bertanya. 😊",
        "Terima kasih kembali! Saya selalu siap membantu. 😊",
        "Senang bisa membantu! Jika butuh info lainnya, tanyakan saja ya.",
    ],
    "unknown": [
        "Mohon maaf, saya tidak mengerti pertanyaan kakak.",
        "Saya kurang memahami maksud pertanyaan kakak. Bisa dijelaskan lebih lanjut?",
        "Hmm... Saya belum bisa menjawab pertanyaan itu. Mungkin kakak bisa bertanya dengan cara lain?",
    ],
    "stok": [
        {"nama": "COMBED 30S", "warna": "HIJAU", "stok": 10, "satuan": "ROLL", "cabang": "HOLIS"},
        {"nama": "COMBED 30S", "warna": "BIRU", "stok": 10, "satuan": "ROLL", "cabang": "KEBON JUKUT"},
        {"nama": "COMBED 30S", "warna": "HIJAU", "stok": 10, "satuan": "Kg", "cabang": "HOLIS"},
        {"nama": "COMBED 30S", "warna": "BIRU", "stok": 10, "satuan": "Kg", "cabang": "KEBON JUKUT"},
        {"nama": "COMBED 24S", "warna": "BIRU", "stok": 10, "satuan": "Kg", "cabang": "KEBON JUKUT"},
    ],
    "data_kain": ["COMBED 30S", "COMBED 24S", "CARDED 24S"],
}
