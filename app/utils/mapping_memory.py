import io
import csv


def mapping_data_stok(data_stok):
    ringkasan = []
    for item in data_stok:
        ringkasan.append(
            {
                "nama_kain": item["nama_kain"],
                "warna_kain": item["warna_kain"],
                "stok": item["stok"],
                "satuan": item["satuan"],
                "cabang": item["cabang"],
            }
        )

    # try:
    #     with io.StringIO() as output:
    #         fieldnames = ["nama_kain", "warna_kain", "stok", "satuan", "cabang"]
    #         writer = csv.DictWriter(output, fieldnames=fieldnames)

    #         writer.writeheader()
    #         for item in ringkasan:
    #             writer.writerow(item)

    #         csv_string = output.getvalue()
    #         return csv_string

    # except Exception as e:
    #     print(f"Terjadi kesalahan saat memformat ke CSV: {e}")
    #     return None

    return ringkasan


def mapping_data_status_order(data):
    ringkasan = []
    for item in data:
        ringkasan.append(
            {"no_order": item["no_order"], "status_order": item["status_order"]}
        )

    # try:
    #     with io.StringIO() as output:
    #         fieldnames = ["nama_kain", "warna_kain", "stok", "satuan", "cabang"]
    #         writer = csv.DictWriter(output, fieldnames=fieldnames)

    #         writer.writeheader()
    #         for item in ringkasan:
    #             writer.writerow(item)

    #         csv_string = output.getvalue()
    #         return csv_string

    # except Exception as e:
    #     print(f"Terjadi kesalahan saat memformat ke CSV: {e}")
    #     return None

    return ringkasan


def mapping_memory(intent: str, data):
    if intent == "stok":
        return mapping_data_stok(data)
    elif intent == "status_order":
        return mapping_data_status_order(data)
