import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KB_FILE_PATH = os.path.join(DATA_DIR, "knowledge_base.json")
DB_PATH = os.path.join(BASE_DIR, "supportpilot_m2.db")

# RAG Thresholds (from Slide 15)
MIN_RELEVANCE_THRESHOLD = 0.30  # Minimum cosine similarity score to qualify as relevant
TOP_K_DOCUMENTS = 3