"""
OmniRead - Word Replacement Module

Member 2
Provides simpler alternatives for difficult words.
"""

WORD_REPLACEMENTS = {
    # Medical / academic
    "pharmaceutical": "drug-related",
    "intervention": "treatment",
    "mitigating": "reducing",
    "cardiovascular": "heart-related",
    "hypertension": "high blood pressure",
    "abnormalities": "problems",
    "efficacy": "effectiveness",
    "complications": "problems",
    "statistically": "measurably",
    "methodology": "method",
    "utilized": "used",
    "demonstrated": "showed",
    "approximately": "about",
    "individuals": "people",
    "subsequently": "later",
    "sufficient": "enough",
    "numerous": "many",
    "obtain": "get",
    "require": "need",
    "assist": "help",
    "assistance": "help",
    "additional": "extra",
    "alternative": "different",
    "commence": "begin",
    "terminate": "end",
    "modify": "change",
    "indicate": "show",
    "implement": "carry out",
    "purchase": "buy",
    "approximately": "about",
    "prior": "before",
    "subsequent": "later",
    "predominantly": "mostly",
    "frequently": "often",
    "occasionally": "sometimes",
    "therefore": "so",
    "however": "but",
    "consequently": "as a result",
    "regarding": "about",
    "concerning": "about",
    "commonly": "usually",
    "numerous": "many",
    "facilitate": "help",
    "indicate": "show",
    "construct": "build",
    "preserve": "keep",
    "terminate": "end",
    "approximately": "about",
    "subsequently": "later",
    "utilize": "use",
}


def get_replacement(word: str, lemma: str | None = None) -> str | None:
    """
    Return a simpler replacement for a difficult word.
    """

    word_lower = word.lower()

    if word_lower in WORD_REPLACEMENTS:
        return WORD_REPLACEMENTS[word_lower]

    if lemma:
        lemma_lower = lemma.lower()

        if lemma_lower in WORD_REPLACEMENTS:
            return WORD_REPLACEMENTS[lemma_lower]

    return None