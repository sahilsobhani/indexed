from ingest import clone_repo
from utils import get_code_files
from chunker import chunk_python_file
from embedder import get_embedding
from indexer import add_chunks, save_index
from qa import ask


def build_index(repo_url):
    repo_path  =  clone_repo(repo_url)
    files = get_code_files(repo_path)

    all_chunks = []
    all_embeddings = []

    for file in files:
        try:
            chunks = chunk_python_file(file)

            for chunk in chunks:
                embedding = get_embedding(chunk["content"])

                chunk["file"] = str(file)

                all_chunks.append(chunk)
                all_embeddings.append(embedding)

        except Exception as e:
            print(f"Skipping {file}: {e}")

    add_chunks(all_chunks, all_embeddings)
    save_index()
    print("Index Built Succesfully")


if __name__ == "__main__":
    repo_url = input("GITHUB REPO URL: ")

    build_index(repo_url)

    while True:
        question = input("\nAsk a question: ")

        if question.lower() == "exit":
            break

        answer = ask(question)

        print("\nANSWER:\n")
        print(answer)

