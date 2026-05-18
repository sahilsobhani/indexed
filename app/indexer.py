import faiss
import json
import numpy as np
from pathlib import Path

INDEX_PATH = "storage/code.index"
METADATA_PATH = "storage/metadata.json"
DEFAULT_INDEX_TYPE = "flat"

dimension = 1536

index = None

metadata_store = []

def create_index(index_type=DEFAULT_INDEX_TYPE):
    """Create a FAISS index for the selected index type."""
    if index_type == "hnsw":
        hnsw_index = faiss.IndexHNSWFlat(dimension, 32)
        hnsw_index.hnsw.efConstruction = 40
        hnsw_index.hnsw.efSearch = 16
        return hnsw_index

    return faiss.IndexFlatL2(dimension)

def initialize_index(index_type=DEFAULT_INDEX_TYPE):
    """Initialize the global FAISS index with the selected type."""
    global index
    global metadata_store

    index = create_index(index_type)
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

