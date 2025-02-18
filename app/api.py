from flask import Flask, request, jsonify
from config.settings import GOOGLE_API_KEY
import google.generativeai as genai
from config.meilisearch_client import meiliClient

app = Flask(__name__)

genai.configure(api_key=GOOGLE_API_KEY)


@app.route("/api/embedding", methods=["POST"])
def buat_embedding():
    try:
        index = meiliClient.index("stok")
        data = index.search("", {"limit": 10})
        data_masuk = data["hits"]
        print(data_masuk)

        embeddings = []
        for item in data_masuk:
            if not all(key in item for key in ["nama_kain", "warna_kain", "cabang"]):
                return (
                    jsonify(
                        {
                            "error": 'Setiap item harus memiliki field "nama_kain", "warna_kain", dan "cabang"'
                        }
                    ),
                    400,
                )

            teks = f"{item['nama_kain']} {item['warna_kain']} {item['cabang']}"

            model = genai.GenerativeModel("embedding-004")
            response = model.embed_content(teks)
            embedding = response.embedding

            embeddings.append(
                {
                    "id": item.get("id"),
                    "nama_kain": item["nama_kain"],
                    "warna_kain": item["warna_kain"],
                    "cabang": item["cabang"],
                    "embedding": embedding,
                }
            )

        return jsonify({"embeddings": embeddings}), 200

    except Exception as e:
        return (
            jsonify({"error": str(e)}),
            400,
        )


if __name__ == "__main__":
    app.run(debug=True)  # Jalankan aplikasi Flask dalam mode debug
