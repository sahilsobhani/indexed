# Indexed

`Indexed` is a small MVP for asking questions about a codebase with retrieval-augmented generation.

It:

- clones a GitHub repository locally
- finds code files
- chunks Python functions with `ast`
- creates embeddings for those chunks
- stores them in a FAISS index
- retrieves relevant chunks for a question
- asks an OpenAI chat model to answer using that retrieved context

## Requirements

- Python 3.10+
- An OpenAI API key

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

## Run

From the project root:

```bash
python app/main.py
```

You will be prompted for:

- a GitHub repository URL
- follow-up questions about that repo

Type `exit` to stop the interactive Q&A loop.

## Current MVP scope

- indexing currently works on Python files
- embeddings use `text-embedding-3-small`
- answers use `gpt-4.1-mini`

## Project structure

- `app/main.py`: CLI entrypoint and indexing flow
- `app/ingest.py`: clone repositories
- `app/utils.py`: collect code files
- `app/chunker.py`: extract Python function chunks
- `app/embedder.py`: create embeddings
- `app/indexer.py`: save and load the FAISS index
- `app/retriever.py`: retrieve relevant chunks
- `app/qa.py`: generate answers from retrieved context
