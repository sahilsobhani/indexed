import faiss
import json
import numpy as np
from pathlib import Path

INDEX_PATH = "storage/code.index"
METADATA_PATH = "storage/metadata.json"

dimension = 1536

index = faiss.IndexFlatL2(dimension)

metadata_store = []

def add_chunks(chunks, embeddings):
    """Add embedded chunks to the in-memory FAISS index and metadata store."""
    global metadata_store

    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)
    metadata_store.extend(chunks)


def save_index():
    """Persist the FAISS index and metadata to disk."""
    Path("storage").mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata_store,f,indent = 2)


def load_index():
    """Load the FAISS index and metadata from disk."""
    global index
    global metadata_store

    index =  faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "r") as f:
        metadata_store = json.load(f)

    return index, metadata_store

