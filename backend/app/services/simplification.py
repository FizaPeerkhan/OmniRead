"""
OmniRead - Text Simplification Module

Member 2 implementation.

Consumes difficult-word analysis produced by Member 1
and generates simplified text.
"""

import re

from app.services.word_replacement import get_replacement


def simplify_difficult_words(
    difficult_words: list[dict]
) -> list[dict]:
    """
    Add replacement suggestions to Member 1's
    difficult-word analysis.
    """

    results = []

    for item in difficult_words:

        word = item.get("word", "")
        lemma = item.get("lemma")

        replacement = get_replacement(
            word,
            lemma
        )

        result = dict(item)

        result["replacement"] = replacement

        results.append(result)

    return results


def replace_words(
    text: str,
    difficult_words: list[dict]
) -> str:
    """
    Replace difficult words with simpler alternatives.
    """

    simplified_text = text

    for item in difficult_words:

        word = item.get("word")
        replacement = item.get("replacement")

        if not word or not replacement:
            continue

        pattern = r"\b" + re.escape(word) + r"\b"

        simplified_text = re.sub(
            pattern,
            replacement,
            simplified_text,
            flags=re.IGNORECASE
        )

    return simplified_text


def simplify_text(
    text: str,
    difficult_words: list[dict]
) -> dict:
    """
    Complete word-level simplification pipeline.
    """

    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    suggestions = simplify_difficult_words(
        difficult_words
    )

    simplified = replace_words(
        text,
        suggestions
    )

    return {
        "original_text": text,
        "simplified_text": simplified,
        "word_replacements": suggestions,
        "simplification_applied": simplified != text
    }