"""
====================================================
OmniRead - Text Statistics Module
====================================================

Calculates descriptive statistics of input text.

Author : Member 1
Project : OmniRead
"""

import textstat

from app.services.preprocessing import preprocess


# ==================================================
# STATISTICS
# ==================================================

def calculate_statistics(text: str) -> dict:
    """
    Calculate descriptive statistics for text.
    """

    if not text:
        raise ValueError("Input text cannot be empty.")

    processed = preprocess(text)

    tokens = processed.tokens
    filtered = processed.filtered_words
    sentences = processed.sentences

    character_count = len(text)

    word_count = len(tokens)

    sentence_count = len(sentences)

    unique_words = len(set(word.lower() for word in tokens))

    average_word_length = (
        sum(len(word) for word in tokens) / word_count
        if word_count > 0
        else 0
    )

    average_sentence_length = (
        word_count / sentence_count
        if sentence_count > 0
        else 0
    )

    total_syllables = textstat.syllable_count(text)

    average_syllables_per_word = (
        total_syllables / word_count
        if word_count > 0
        else 0
    )

    lexical_density = (
        len(filtered) / word_count
        if word_count > 0
        else 0
    )

    return {

        "character_count": character_count,

        "word_count": word_count,

        "sentence_count": sentence_count,

        "unique_words": unique_words,

        "average_word_length": round(
            average_word_length,
            2
        ),

        "average_sentence_length": round(
            average_sentence_length,
            2
        ),

        "average_syllables_per_word": round(
            average_syllables_per_word,
            2
        ),

        "lexical_density": round(
            lexical_density,
            2
        )

    }


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    sample = """
    The pharmaceutical intervention demonstrated statistically
    significant efficacy in mitigating cardiovascular complications
    among patients with chronic hypertension.
    """

    result = calculate_statistics(sample)

    print("=" * 60)
    print("TEXT STATISTICS")
    print("=" * 60)

    for key, value in result.items():

        print(f"{key:35}: {value}")