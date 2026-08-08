"""
====================================================
OmniRead - Readability Analysis Module
====================================================

Calculates multiple readability metrics for a given text.

Author : Member 1
Project : OmniRead
"""

import textstat


# ==================================================
# Difficulty Label
# ==================================================



def overall_difficulty(report):
    score = 0

    if report["flesch_reading_ease"] < 30:
        score += 2
    elif report["flesch_reading_ease"] < 60:
        score += 1

    if report["gunning_fog"] > 18:
        score += 2
    elif report["gunning_fog"] > 12:
        score += 1

    if report["flesch_kincaid_grade"] > 12:
        score += 2
    elif report["flesch_kincaid_grade"] > 8:
        score += 1

    if score >= 5:
        return "Very Difficult"
    elif score >= 3:
        return "Difficult"
    elif score >= 2:
        return "Moderate"
    else:
        return "Easy"

# ==================================================
# Readability Metrics
# ==================================================
    
def calculate_readability(text: str) -> dict:
    """
    Calculate readability metrics for the given text.
    """

    if not text:
        raise ValueError("Input text cannot be empty.")

    report = {
        "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 2),

        "flesch_kincaid_grade": round(
            textstat.flesch_kincaid_grade(text), 2
        ),

        "gunning_fog": round(
            textstat.gunning_fog(text), 2
        ),

        "smog_index": round(
            textstat.smog_index(text), 2
        ),

        "coleman_liau_index": round(
            textstat.coleman_liau_index(text), 2
        ),

        "automated_readability_index": round(
            textstat.automated_readability_index(text), 2
        ),

        "dale_chall_score": round(
            textstat.dale_chall_readability_score(text), 2
        ),

        "linsear_write_formula": round(
            textstat.linsear_write_formula(text), 2
        ),

        "reading_time_seconds": round(
            textstat.reading_time(text), 2
        ),
    }

    # Add overall difficulty after computing all metrics
    report["difficulty"] = overall_difficulty(report)

    return report


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    sample = """
The cat sat on the mat.
"""

    result = calculate_readability(sample)

    print("=" * 60)

    print("READABILITY REPORT")

    print("=" * 60)

    for key, value in result.items():

        print(f"{key:35}: {value}")