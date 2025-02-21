import io
import csv


def mapping_data_stok(data_stok):
    result = []
    for item in data_stok:
        result.append(
            {
                "nama_kain": item["nama_kain"],
                "warna_kain": item["warna_kain"],
                "stok": item["stok"],
                "satuan": item["satuan"],
                "cabang": item["cabang"],
            }
        )

    try:
        with io.StringIO() as output:
            fieldnames = ["nama_kain", "warna_kain", "stok", "satuan", "cabang"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            writer.writeheader()
            for item in result:
                writer.writerow(item)

            csv_string = output.getvalue()
            return csv_string

    except Exception as e:
        print(f"Terjadi kesalahan saat memformat ke CSV: {e}")
        return result


def mapping_data_status_order(data):
    result = []
    for item in data:
        result.append(
            {"no_order": item["no_order"], "status_order": item["status_order"], "tagihan": item["tagihan"],"ongkir": item["ongkir"]}
        )

    try:
        with io.StringIO() as output:
            fieldnames = ["no_order", "status_order", "tagihan", "ongkir"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            writer.writeheader()
            for item in result:
                writer.writerow(item)

            csv_string = output.getvalue()
            return csv_string

    except Exception as e:
        print(f"Terjadi kesalahan saat memformat ke CSV: {e}")
        return result


def mapping_data_price(data):
    result = []
    for item in data:
        result.append(
            {
                "nama_kain": item["nama_kain"],
                "warna_kain": item["warna_kain"],
                "harga_rollan": item["harga_rollan"],
                "harga_diatas": item["harga_diatas"],
                "harga_dibawah": item["harga_dibawah"],
                "cabang": item["cabang"],
            }
        )

    try:
        with io.StringIO() as output:
            fieldnames = [
                "nama_kain",
                "warna_kain",
                "harga_rollan",
                "harga_diatas",
                "harga_dibawah",
                "cabang",
            ]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            writer.writeheader()
            for item in result:
                writer.writerow(item)

            csv_string = output.getvalue()
            return csv_string

    except Exception as e:
        print(f"Terjadi kesalahan saat memformat ke CSV: {e}")
        return result

def mapping_data_resi(data):
    result = []
    for item in data:
        if item.get("no_resi"):
            result.append(
                {"no_order": item["no_order"], "no_resi": item["no_resi"]}
            )

    try:
        with io.StringIO() as output:
            fieldnames = ["no_order", "no_resi"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            writer.writeheader()
            for item in result:
                writer.writerow(item)

            csv_string = output.getvalue()
            return csv_string

    except Exception as e:
        print(f"Terjadi kesalahan saat memformat ke CSV: {e}")
        return result


def mapping_memory(intent: str, data):
    # if intent == "stok":
    #     return mapping_data_stok(data)
    # elif intent == "status_order":
    #     return mapping_data_status_order(data)
    # elif intent == "price_list":
    #     return mapping_data_price(data)
    # elif intent == 'cek_resi':
    #     return mapping_data_resi(data)
    # else:
    #     return data
    
    return data
