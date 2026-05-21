import json
from pathlib import Path

from db import get_collection
from embedder import get_embedding
from indexer import (
    DEFAULT_INDEX_TYPE,
    add_chunks as add_faiss_chunks,
    initialize_index,
    load_index,
    save_index,
)

DEFAULT_VECTOR_BACKEND = "faiss"
BACKEND_CONFIG_PATH = Path("storage/backend.json")

_active_backend = DEFAULT_VECTOR_BACKEND


def save_active_backend(backend):
    """Persist the selected vector backend for future retrieval."""
    BACKEND_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(BACKEND_CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump({"backend": backend}, file, indent=2)


def load_active_backend():
    """Load the current vector backend from disk."""
    if not BACKEND_CONFIG_PATH.exists():
        return DEFAULT_VECTOR_BACKEND

    with open(BACKEND_CONFIG_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("backend", DEFAULT_VECTOR_BACKEND)


def initialize_store(backend=DEFAULT_VECTOR_BACKEND, index_type=DEFAULT_INDEX_TYPE):
    """Initialize the selected vector backend."""
    global _active_backend

    _active_backend = backend

    if backend == "chroma":
        collection = get_collection()
        existing_count = collection.count()
        if existing_count:
            ids = collection.get(include=[])["ids"]
            collection.delete(ids=ids)
    else:
        initialize_index(index_type)


def add_chunks(chunks, embeddings, backend=None):
    """Add chunks and embeddings to the selected vector backend."""
    backend = backend or _active_backend

    if backend == "chroma":
        collection = get_collection()
        ids = []
        metadatas = []
        documents = []

        for idx, chunk in enumerate(chunks):
            ids.append(
                f"{chunk.get('file_path', 'unknown')}::{chunk.get('name', 'chunk')}::{idx}"
            )
            metadatas.append(
                {
                    "type": str(chunk.get("type", "unknown")),
                    "name": str(chunk.get("name", "unknown")),
                    "file_name": str(chunk.get("file_name", "unknown")),
                    "file_path": str(chunk.get("file_path", "unknown")),
                }
            )
            documents.append(chunk.get("content", ""))

        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
        )
        return

    add_faiss_chunks(chunks, embeddings)


def save_store(backend=None):
    """Persist the selected backend if needed and remember it for retrieval."""
    backend = backend or _active_backend
    save_active_backend(backend)

    if backend == "faiss":
        save_index()


def search_store(query, k=5):
    """Search the selected backend and return chunk-shaped results."""
    backend = load_active_backend()
    query_embedding = get_embedding(query)

    if backend == "chroma":
        collection = get_collection()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["metadatas", "documents"],
        )

        chunks = []
        metadatas = results.get("metadatas", [[]])[0]
        documents = results.get("documents", [[]])[0]

        for metadata, document in zip(metadatas, documents):
            chunk = dict(metadata or {})
            chunk["content"] = document or ""
            chunks.append(chunk)

        return chunks

    index, metadata = load_index()
    import numpy as np

    vector = np.array([query_embedding]).astype("float32")
    _distance, indices = index.search(vector, k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(metadata):
            results.append(metadata[idx])

    return results
