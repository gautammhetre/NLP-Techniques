"""Create embeddings with Sentence Transformers."""
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_texts(texts):
    """Embed a list of strings -> list of vectors (normalized)."""
    return _get_model().encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()


def embed_query(text):
    return embed_texts([text])[0]
