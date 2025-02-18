from config.meilisearch_client import meiliClient


def get_data_meili(type: str):
    index = meiliClient.index("kamus_kata")
    filter_cond = f"""type = '{type}'"""
    search_results = index.search("", {"filter": filter_cond, "limit": 1000})

    return set(result["name"].lower() for result in search_results["hits"])


def preprocessing_text(text: str, intent: str) -> str:
    fabric_related_intent = ["stok", "price_list"]

    text = text.lower()
    words = text.split()

    relevant_words = []
    data_lexicon = []
    if intent in fabric_related_intent:
        data_lexicon = get_data_meili("kain")

    for word in words:
        if word in data_lexicon:
            relevant_words.append(word)

    processed_text = " ".join(relevant_words)

    return processed_text
