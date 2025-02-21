from config.meilisearch_client import meiliClient
# from spellchecker import SpellChecker


def get_data_meili(type: str):
    index = meiliClient.index("kamus_kata")
    filter_cond = f"""type = '{type}'"""
    search_results = index.search("", {"filter": filter_cond, "limit": 1000})

    return set(result["word"].lower() for result in search_results["hits"])


def preprocessing_text(text: str, intent: str) -> str:
    fabric_related_intent = ["stok", "price_list"]

    # spell = SpellChecker()

    text = text.lower()
    words = text.split()

    corrected_words = words

    relevant_words = []
    data_lexicon = []

    if intent in fabric_related_intent:
        data_lexicon.extend(get_data_meili("kain"))
        data_lexicon.extend(get_data_meili("warna"))
    else:
        data_lexicon.extend(get_data_meili('faq'))
        
    sorted_lexicon = sorted(data_lexicon, key=lambda x: len(x.split()), reverse=True)

    used_words = set()

    for phrase in sorted_lexicon:
        phrase_words = phrase.split()
        if all(
            word in corrected_words and word not in used_words for word in phrase_words
        ):
            relevant_words.append(phrase)
            used_words.update(phrase_words)

    processed_text = " ".join(relevant_words)

    return processed_text
