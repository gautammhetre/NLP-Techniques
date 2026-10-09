"""Project configuration: paths, model names and retrieval settings."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Paths
DATASET_DIR = BASE_DIR / "dataset"
VECTOR_DB_DIR = BASE_DIR / "vector_store"
COLLECTION_NAME = "pdf_chunks"

# Groq LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunking (in words)
CHUNK_SIZE = 200
CHUNK_OVERLAP = 40

# Retrieval
TOP_K = 6                 # chunks for a normal question
TOP_K_PER_DOC = 3         # chunks per document for multi-document questions
MAX_DISTANCE = 0.75       # cosine distance; chunks farther than this are ignored
MAX_DOC_CONTEXT_CHARS = 12000  # text sent to the LLM for insight / summary
MIN_DOC_CHARS = 300       # documents with less text are treated as too short

# Memory
MEMORY_TURNS = 4          # number of previous Q&A pairs kept for follow-ups
