from rapidfuzz import process


def correct_typo_with_rapidfuzz(text):
    correct_words = ["combed", "30s", "maroon", "carded", "24s"]
    words = text.split()
    corrected_words = []

    for word in words:
        match = process.extractOne(word, correct_words)
        if match and match[1] > 80:
            corrected_words.append(match[0])
        else:
            corrected_words.append(word)

    corrected_text = " ".join(corrected_words)
    return corrected_text
