import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from app.config.meilisearch_client import meiliClient
from fuzzywuzzy import fuzz


def get_kamus_kata(intent=""):
    index = meiliClient.index("kamus_kata")

    def get_data_meili(type=""):
        filter_cond = f"""type = {type}"""
        search_results = index.search("", {"filter": filter_cond, "limit": 2000})

        return (
            result["text"].strip().lower()
            for result in search_results["hits"]
            if result["text"].strip()
        )

    fabric_related_intent = ["stok", "price_list"]

    data_lexicon = set()

    if intent in fabric_related_intent:
        data_lexicon.update(get_data_meili("kain"))
    elif intent == "faq":
        data_lexicon.update(get_data_meili("faq"))
    else:
        data_lexicon.update(get_data_meili("fitur"))

    return data_lexicon


def find_similar_text(lower_text, data_lexicon):
    highest_similarity = 0
    best_match = None

    def calculate_char_match(str1, str2):
        common_chars = sum(1 for c in str1 if c in str2)
        return common_chars / max(len(str1), len(str2)) * 100

    for phrase in data_lexicon:
        if lower_text == phrase:
            similarity = 100
            char_similarity = 100
        else:
            similarity = fuzz.partial_ratio(lower_text, phrase)
            char_similarity = calculate_char_match(lower_text, phrase)

        combined_similarity = (similarity + char_similarity) / 2

        if combined_similarity > highest_similarity:
            highest_similarity = combined_similarity
            best_match = phrase

    if highest_similarity > 65 and best_match != " ":
        print("highest similarity:", highest_similarity)
        return best_match
    else:
        return None


def tokenize(text: str):
    return text.split()


def load_stopwords(file_path):
    with open(file_path, "r") as file:
        stopwords = file.read().splitlines()
    return set(stopwords)


def remove_stopwords(tokens: list):
    stopwords = load_stopwords("app/data/stopwords_id.txt")

    filtered_words = [word for word in tokens if word not in stopwords]

    return filtered_words


def lower_casing(tokens: list):
    return [token.lower() for token in tokens]


def remove_punctuation(tokens: list):
    return [
        token.translate(str.maketrans("", "", string.punctuation)) for token in tokens
    ]


def stemming(tokens: list):
    fact = StemmerFactory()
    stemmer = fact.create_stemmer()

    return [stemmer.stem(token) for token in tokens]


def pre_processing(text: str, intent="kain"):
    lower_text = text.lower()
    data_lexicon = get_kamus_kata(intent=intent)
    matched_phrase = find_similar_text(lower_text, data_lexicon)

    if matched_phrase:
        print("MTC", matched_phrase)
        return matched_phrase
    else:
        tokens = tokenize(text=text)
        tokens = lower_casing(tokens=tokens)
        tokens = remove_stopwords(tokens=tokens)
        tokens = remove_punctuation(tokens=tokens)
        tokens = stemming(tokens=tokens)

        sentence = " ".join(tokens)
        print("st", sentence)
        matched_phrase = find_similar_text(sentence, data_lexicon)

        return matched_phrase
