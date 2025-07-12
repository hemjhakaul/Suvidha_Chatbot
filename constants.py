import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Persistence directories
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_store")
SAVE_DIR = os.path.join(BASE_DIR, "uploaded_pdfs")
CHAT_HISTORY_DIR = os.path.join(BASE_DIR, "chat_history")
FILE_LOG = os.path.join(PERSIST_DIR, "uploaded_files.txt")

# Create directories if not exist
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(PERSIST_DIR, exist_ok=True)
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

# Model configurations
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "mistral"
LLM_CONFIG = {
    "temperature": 0.1,
    "top_p": 0.9,
    "num_ctx": 2048
}

# Text splitter config
TEXT_SPLITTER_CONFIG = {
    "chunk_size": 3000,
    "chunk_overlap": 200
}