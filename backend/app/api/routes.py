"""
====================================================
OmniRead API Routes
====================================================
"""

from fastapi import APIRouter

from app.models.request_models import TextRequest

from app.services.preprocessing import preprocess
from app.services.readability import calculate_readability
from app.services.statistics import calculate_statistics
from app.services.difficult_words import detect_difficult_words
from app.services.complex_sentences import detect_complex_sentences
from app.services.simplification import simplify_text

router = APIRouter()


@router.post("/analyze")
def analyze_text(request: TextRequest):

    text = request.text

    processed = preprocess(text)

    return {

        "preprocessing": {

            "cleaned_text": processed.cleaned_text,

            "sentences": processed.sentences,

            "tokens": processed.tokens,

            "filtered_words": processed.filtered_words,

            "lemmas": processed.lemmas,

            "pos_tags": processed.pos_tags,

            "named_entities": processed.named_entities

        },

        "readability": calculate_readability(text),

        "statistics": calculate_statistics(text),

        "difficult_words": detect_difficult_words(text),

        "complex_sentences": detect_complex_sentences(text)

    }

@router.post("/simplify")
def simplify_text_endpoint(request: TextRequest):

    text = request.text

    # Get Member 1's difficult-word analysis
    difficult_words = detect_difficult_words(text)

    # Send Member 1's output to Member 2
    result = simplify_text(
        text,
        difficult_words
    )

    return result