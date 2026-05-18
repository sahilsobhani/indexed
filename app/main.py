from ingest import clone_repo
from utils import get_code_files
from chunker import chunk_python_file
from embedder import get_embedding
from indexer import add_chunks, save_index
from qa import ask, load_conversation, save_conversation

SEPARATOR = "--" * 60


def build_index(repo_url):
    """Build embeddings and metadata for all supported code files in a repo."""
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

    add_chunks(all_chunks, all_embeddings)
    save_index()
    print("Index Built Succesfully")


if __name__ == "__main__":
    repo_url = input("GITHUB REPO URL: ")

    build_index(repo_url)
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
