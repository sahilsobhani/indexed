from ingest import clone_repo
from utils import get_code_files
from chunker import chunk_python_file
from embedder import get_embedding
from indexer import DEFAULT_INDEX_TYPE
from qa import ask, load_conversation, save_conversation
from banner import print_banner
from vector_store import add_chunks, initialize_store, save_store

SEPARATOR = "--" * 60
DEFAULT_VECTOR_BACKEND = "faiss"
SUPPORTED_VECTOR_BACKENDS = {"faiss", "chroma"}


def choose_vector_backend():
    """Prompt the user to choose a vector backend."""
    selection = input(
        f"Choose vector backend [faiss/chroma] (default: {DEFAULT_VECTOR_BACKEND}): "
    ).strip().lower()

    if selection in SUPPORTED_VECTOR_BACKENDS:
        print(f"Using {selection.upper()} backend")
        return selection

    print(f"Using {DEFAULT_VECTOR_BACKEND.upper()} backend")
    return DEFAULT_VECTOR_BACKEND


def choose_index_type():
    """Prompt the user to choose an index type."""
    selection = input(
        f"Choose FAISS index type [flat/hnsw] (default: {DEFAULT_INDEX_TYPE}): "
    ).strip().lower()

    if selection in {"flat", "hnsw"}:
        print(f"Building {selection.upper()} Index")
        return selection
    
    print(f"Building FLAT Index")
    return DEFAULT_INDEX_TYPE

def build_index(
    repo_url,
    backend=DEFAULT_VECTOR_BACKEND,
    index_type=DEFAULT_INDEX_TYPE,
):
    """Build embeddings and metadata for all supported code files in a repo."""
    initialize_store(backend, index_type)

    repo_path  =  clone_repo(repo_url)
    files = get_code_files(repo_path)
    python_files = [file for file in files if str(file).endswith(".py")]

    all_chunks = []
    all_embeddings = []

    for file in python_files:
        try:
            chunks = chunk_python_file(file)

            for chunk in chunks:
                embedding = get_embedding(chunk["content"])

                all_chunks.append(chunk)
                all_embeddings.append(embedding)

        except Exception as e:
            print(f"Skipping {file}: {e}")

    if not all_chunks:
        print("No Python chunks found to index.")
        return

    add_chunks(all_chunks, all_embeddings, backend)
    
    save_store(backend)
    print("Index Built Succesfully")


if __name__ == "__main__":
    print_banner()
    repo_url = input("GITHUB REPO URL: ")
    backend = choose_vector_backend()
    index_type = choose_index_type() if backend == "faiss" else DEFAULT_INDEX_TYPE

    build_index(repo_url, backend, index_type)
    history = load_conversation()

    while True:
        question = input("\nAsk a question: ").strip()

        if question.lower() == "exit":
            break

        if question.lower() == "clear":
            history = []
            save_conversation(history)
            print("\nConversation history cleared.")
            continue

        answer = ask(question, history)

        print("\nANSWER:\n")
        print(answer)
        print(f"\n{SEPARATOR}")
