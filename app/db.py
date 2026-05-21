from pathlib import Path

import chromadb

CHROMA_PATH = Path("storage/chroma")
COLLECTION_NAME = "indexed"


def get_client():
    """Return a persistent local Chroma client."""
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PATH))


def get_collection(name=COLLECTION_NAME):
    """Return the Chroma collection used by Indexed."""
    client = get_client()
    return client.get_or_create_collection(name=name)
