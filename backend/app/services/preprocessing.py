"""
====================================================
OmniRead - Text Preprocessing Module
====================================================

This module performs all preprocessing tasks required
before readability analysis and text simplification.

Author : Member 1
Project : OmniRead
"""

import re
from dataclasses import dataclass

import spacy
from spacy.tokens import Doc
from nltk.corpus import stopwords


# --------------------------------------------------
# Load spaCy model (loaded only once)
# --------------------------------------------------

nlp = spacy.load("en_core_web_sm")

# --------------------------------------------------
# Load stopwords
# --------------------------------------------------

STOP_WORDS = set(stopwords.words("english"))


# ==================================================
# DATA CLASS
# ==================================================
from spacy.tokens import Span

@dataclass
class ProcessedText:
    #stores the results of preprocessing steps
    doc: Doc
    cleaned_text: str
    sentences: list[str]
    sentence_spans: list[Span]
    tokens: list[str]
    filtered_words: list[str]
    lemmas: list[str]
    pos_tags: list[dict]
    named_entities: list[dict]


# ==================================================
# TEXT CLEANING
# ==================================================

def clean_text(text: str) -> str:
    """
    Clean raw input text.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
        Cleaned text.
    """

    if text is None:
        raise ValueError("Input text cannot be None.")

    text = str(text)

    # Remove extra spaces, tabs and newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==================================================
# SENTENCE SEGMENTATION
# ==================================================

def sentence_segmentation(doc: Doc) -> list[str]:
    """
    Split text into sentences.
    """

    return [sentence.text for sentence in doc.sents]


# ==================================================
# TOKENIZATION
# ==================================================

def tokenize(doc: Doc) -> list[str]:
    """
    Convert document into alphabetic tokens.
    """

    return [
        token.text
        for token in doc
        if token.is_alpha
    ]


# ==================================================
# STOPWORD REMOVAL
# ==================================================

def remove_stopwords(words: list[str]) -> list[str]:
    """
    Remove English stopwords.
    """

    return [
        word
        for word in words
        if word.lower() not in STOP_WORDS
    ]


# ==================================================
# LEMMATIZATION
# ==================================================

def lemmatize(doc: Doc) -> list[str]:
    """
    Convert words to their base form.
    """

    return [
        token.lemma_
        for token in doc
        if token.is_alpha
    ]


# ==================================================
# POS TAGGING
# ==================================================

def pos_tagging(doc: Doc) -> list[dict]:
    """
    Generate Part-of-Speech information.
    """

    pos_data = []

    for token in doc:

        if token.is_alpha:

            pos_data.append(
                {
                    "word": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "dependency": token.dep_,
                }
            )

    return pos_data


# ==================================================
# NAMED ENTITY RECOGNITION
# ==================================================

def named_entity_recognition(doc: Doc) -> list[dict]:
    """
    Extract named entities.
    """

    entities = []

    for entity in doc.ents:

        entities.append(
            {
                "entity": entity.text,
                "label": entity.label_,
            }
        )

    return entities


# ==================================================
# MASTER FUNCTION
# ==================================================

def preprocess(text: str) -> ProcessedText:
    """
    Complete preprocessing pipeline.

    Parameters
    ----------
    text : str

    Returns
    -------
    ProcessedText
    """

    cleaned = clean_text(text)

    doc = nlp(cleaned)

    sentences = sentence_segmentation(doc)

    tokens = tokenize(doc)

    filtered_words = remove_stopwords(tokens)

    lemmas = lemmatize(doc)

    pos = pos_tagging(doc)

    entities = named_entity_recognition(doc)
    sentence_spans = list(doc.sents)

    return ProcessedText(
    doc=doc,
    cleaned_text=cleaned,
    sentences=sentences,
    sentence_spans=sentence_spans,
    tokens=tokens,
    filtered_words=filtered_words,
    lemmas=lemmas,
    pos_tags=pos,
    named_entities=entities
    )
    


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    sample = """
    The pharmaceutical intervention demonstrated statistically
    significant efficacy in mitigating cardiovascular complications
    among patients with chronic hypertension.
    """

    result = preprocess(sample)

    print("=" * 60)
    print("Cleaned Text")
    print("=" * 60)
    print(result.cleaned_text)

    print("\nSentences")
    print(result.sentences)

    print("\nTokens")
    print(result.tokens)

    print("\nFiltered Words")
    print(result.filtered_words)

    print("\nLemmas")
    print(result.lemmas)

    print("\nPOS Tags")
    for item in result.pos_tags:
        print(item)

    print("\nNamed Entities")
    for entity in result.named_entities:
        print(entity)