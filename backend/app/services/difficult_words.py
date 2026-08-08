"""
====================================================
OmniRead - Difficult Word Detection Module
====================================================

Detects difficult words using multiple linguistic features.

Criteria:
1. Word Frequency (wordfreq)
2. Word Length
3. Number of Syllables

Author : Member 1
Project : OmniRead
"""

from wordfreq import zipf_frequency
import textstat

from app.services.preprocessing import preprocess

# ==================================================
# CONFIGURATION
# ==================================================

MIN_WORD_LENGTH = 10
MAX_ZIPF_FREQUENCY = 3.5
MIN_SYLLABLES = 4

# Common academic words that usually don't require simplification
COMMON_WORDS = {
    "student",
    "students",
    "education",
    "computer",
    "system",
    "research",
    "important",
    "information",
    "different",
    "development",
    "demonstrated",
    "significant",
    "complications"
}


# ==================================================
# DIFFICULTY LEVEL
# ==================================================

def difficulty_level(score: int) -> str:
    """
    Convert numeric score to difficulty level.
    """

    if score >= 4:
        return "High"

    elif score >= 3:
        return "Medium"

    return "Low"


# ==================================================
# DETECT DIFFICULT WORDS
# ==================================================

def detect_difficult_words(text: str) -> list[dict]:
    """
    Detect difficult words from text.

    Parameters
    ----------
    text : str

    Returns
    -------
    list[dict]
    """

    if not text:
        raise ValueError("Input text cannot be empty.")

    processed = preprocess(text)

    difficult_words = []

    seen = set()

    for token in processed.doc:

        if not token.is_alpha:
            continue

        word = token.text
        word_lower = word.lower()

        if word_lower in seen:
            continue

        seen.add(word_lower)

        if word_lower in COMMON_WORDS:
            continue

        score = 0
        reasons = []

        frequency = zipf_frequency(word_lower, "en")
        syllables = textstat.syllable_count(word)

        # -------------------------
        # Rare word (Highest weight)
        # -------------------------
        if frequency < MAX_ZIPF_FREQUENCY:
            score += 2
            reasons.append("Rare word")

        # -------------------------
        # Long word
        # -------------------------
        if len(word) >= MIN_WORD_LENGTH:
            score += 1
            reasons.append("Long word")

        # -------------------------
        # Many syllables
        # -------------------------
        if syllables >= MIN_SYLLABLES:
            score += 1
            reasons.append("Many syllables")

        # -------------------------
        # Keep only difficult words
        # -------------------------
        if score >= 2:

            difficult_words.append({

                "word": word,

                "lemma": token.lemma_,

                "difficulty_score": score,

                "difficulty_level": difficulty_level(score),

                "zipf_frequency": round(frequency, 2),

                "syllables": syllables,

                "start": token.idx,

                "end": token.idx + len(word),

                "reasons": reasons,

                # Filled later by Member 2
                "replacement": None

            })

    difficult_words.sort(

        key=lambda x: (

            x["difficulty_score"],

            -x["zipf_frequency"]

        ),

        reverse=True

    )

    return difficult_words


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    sample = """
    The pharmaceutical intervention demonstrated statistically
    significant efficacy in mitigating cardiovascular
    complications among patients with chronic hypertension.
    """

    result = detect_difficult_words(sample)

    print("=" * 70)
    print("DIFFICULT WORD REPORT")
    print("=" * 70)

    for word in result:

        print(f"\nWord              : {word['word']}")
        print(f"Lemma             : {word['lemma']}")
        print(f"Difficulty Score  : {word['difficulty_score']}")
        print(f"Difficulty Level  : {word['difficulty_level']}")
        print(f"Zipf Frequency    : {word['zipf_frequency']}")
        print(f"Syllables         : {word['syllables']}")
        print(f"Position          : {word['start']} - {word['end']}")
        print(f"Reasons           : {', '.join(word['reasons'])}")