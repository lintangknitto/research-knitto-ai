import re
import time
from utils.pre_processing import pre_processing
from config.meilisearch_client import meiliClient
from utils.mapping_memory import mapping_memory

def get_no_order(text):
    data_cabang = meiliClient.index('cabang').search('')

    list_kode = set()

    for dc in data_cabang['hits']:
        list_kode.add(dc['kode_order'].lower())
        list_kode.add(dc['kode_orderkatalog'].lower())

    text = text.lower()
    words = text.split()

    for word in words:
        for kode in list_kode:
            if word.startswith(kode):
                digits_part = word[len(kode):]
                
                if digits_part.isdigit():
                    return word
    return ""


def get_cabang(text):
    list_cabang = ["HOLIS", "KEBON JUKUT", "SUDIRMAN", "HOS COKROAMINOTO", "SOEKARNO"]

    for cabang in list_cabang:
        if re.search(r"\b" + re.escape(cabang) + r"\b", text, re.IGNORECASE):
            return cabang

    return ""


def get_memory_from_meili(intent: str, question: str, nohp: str, first_intent=""):
    limit = 5
    try:
        list_spesifik_intent = ["stok", "price_list", "faq"]
        query = ""
        if intent in list_spesifik_intent:
            query = pre_processing(text=question, intent=intent)
        
        filter_condition = ""
        print(f"Query yang diproses: {query}")

        index_selected = "unknown"
        if intent == "greetings" or intent == "kanita":
            query = ""
            index_selected = intent
        elif intent == "notfound":
            no_order = get_no_order(question)
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
        elif intent == "status_order" or intent == "cek_resi":
            no_order = get_no_order(question)
            print('NO_ORDER', no_order)
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
        
        print('HASIL FILTER', filter_condition)
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

def get_context(intent: str, question: str, nohp: str, first_intent=""):
    memory = get_memory_from_meili(intent, question, nohp, first_intent)
    
    context = "Tidak terdapat datanya"
    if len(memory) > 0:
        context = mapping_memory(intent=intent, data=memory)
    
    return context