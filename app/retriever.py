import numpy as np

from embedder  import get_embedding
from indexer import load_index

def search(query, k=5):
    """Return the top matching metadata chunks for a query."""
    index, metadata = load_index()

    query_embedding = get_embedding(query)

    vector = np.array([query_embedding]).astype("float32")

    distance, indices = index.search(vector, k)

    results = []

    for idx in indices[0]:
        if 0 <= idx < len(metadata):
            results.append(metadata[idx])

    return results
