from vector_store import search_store

def search(query, k=5):
    """Return the top matching metadata chunks for a query."""
    return search_store(query, k)
