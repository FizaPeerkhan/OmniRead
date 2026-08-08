"""
====================================================
OmniRead - Complex Sentence Detection Module
====================================================

Detects complex sentences using multiple linguistic features.

Author : Member 1
Project : OmniRead
"""

from app.services.preprocessing import preprocess
from app.services.readability import calculate_readability

# ==================================================
# CONFIGURATION
# ==================================================

MAX_SENTENCE_LENGTH = 20
MAX_AVERAGE_WORD_LENGTH = 6
MAX_COMMAS = 2
MIN_DIFFICULT_WORDS = 3


# ==================================================
# DIFFICULTY LEVEL
# ==================================================

def difficulty_level(score: int) -> str:
    """
    Convert numeric score into difficulty level.
    """

    if score >= 4:
        return "High"

    elif score >= 2:
        return "Medium"

    return "Low"


# ==================================================
# DETECT COMPLEX SENTENCES
# ==================================================

def detect_complex_sentences(text: str) -> list[dict]:
    """
    Detect complex sentences using linguistic features.

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

    readability = calculate_readability(text)

    complex_sentences = []

    # ------------------------------------------------
    # Iterate through sentence spans from preprocessing
    # ------------------------------------------------

    for span in processed.sentence_spans:

        sentence = span.text

        words = [

            token.text

            for token in span

            if token.is_alpha

        ]

        word_count = len(words)

        average_word_length = (

            sum(len(word) for word in words) / word_count

            if word_count > 0

            else 0

        )

        comma_count = sentence.count(",")

        difficult_word_count = sum(

            1

            for word in words

            if len(word) >= 10

        )

        score = 0

        reasons = []

        # -----------------------------------------
        # Rule 1 : Long sentence
        # -----------------------------------------

        if word_count > MAX_SENTENCE_LENGTH:

            score += 1

            reasons.append("Long sentence")

        # -----------------------------------------
        # Rule 2 : Long average word length
        # -----------------------------------------

        if average_word_length > MAX_AVERAGE_WORD_LENGTH:

            score += 1

            reasons.append("Long average word length")

        # -----------------------------------------
        # Rule 3 : Many difficult words
        # -----------------------------------------

        if difficult_word_count >= MIN_DIFFICULT_WORDS:

            score += 1

            reasons.append("Many difficult words")

        # -----------------------------------------
        # Rule 4 : Multiple clauses
        # -----------------------------------------

        if comma_count >= MAX_COMMAS:

            score += 1

            reasons.append("Multiple clauses")

        # -----------------------------------------
        # Rule 5 : Low readability
        # -----------------------------------------

        if readability["difficulty"] in [

            "Difficult",

            "Very Difficult"

        ]:

            score += 1

            reasons.append("Low readability")

        # -----------------------------------------
        # Save complex sentence
        # -----------------------------------------

        if score >= 2:

            complex_sentences.append({

                "sentence": sentence,

                "difficulty_score": score,

                "difficulty_level": difficulty_level(score),

                "word_count": word_count,

                "average_word_length": round(
                    average_word_length,
                    2
                ),

                "comma_count": comma_count,

                "difficult_word_count": difficult_word_count,

                "reasons": reasons

            })

    return complex_sentences


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    sample = """
    The pharmaceutical intervention demonstrated statistically
    significant efficacy in mitigating cardiovascular complications
    among patients with chronic hypertension, particularly those
    who had undergone previous surgical procedures, while
    simultaneously reducing adverse outcomes.
    """

    result = detect_complex_sentences(sample)

    print("=" * 70)
    print("COMPLEX SENTENCE REPORT")
    print("=" * 70)

    if not result:

        print("No complex sentences detected.")

    else:

        for sentence in result:

            print("\nSentence:")
            print(sentence["sentence"])

            print("\nDifficulty Level :", sentence["difficulty_level"])
            print("Difficulty Score :", sentence["difficulty_score"])
            print("Word Count       :", sentence["word_count"])
            print("Average Word Len :", sentence["average_word_length"])
            print("Comma Count      :", sentence["comma_count"])
            print("Difficult Words  :", sentence["difficult_word_count"])
            print("Reasons          :", ", ".join(sentence["reasons"]))

            print("-" * 70)