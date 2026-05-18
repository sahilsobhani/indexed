# Indexed

`Indexed` is a small MVP for asking questions about a codebase with retrieval-augmented generation.

It:

- clones a GitHub repository locally
- finds code files
- chunks Python code with `ast`
- creates embeddings for those chunks
- stores them in a FAISS index
- retrieves relevant chunks for a question
- asks an OpenAI chat model to answer using that retrieved context

Today, that includes a few quality-of-life improvements as well:

- chunk metadata includes `file_name` and `file_path`
- chunking covers Python functions plus module-level assignments
- follow-up questions can use saved conversation history
- the CLI can build either a flat FAISS index or an HNSW index
- a small `flush` script clears generated indexes, metadata, conversation history, and cloned repos

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
- a FAISS index type: `flat` or `hnsw`
- follow-up questions about that repo

Pressing Enter at the index prompt uses the default: `flat`.

Inside the Q&A loop:

- type `exit` to stop
- type `clear` to clear saved conversation history

The CLI also prints a simple separator between answers to keep the terminal output cleaner.

## What Gets Indexed

For Python files, the chunker currently stores:

- top-level functions
- module-level constants such as `MAX_RETRIES = 3`
- other module-level assignments such as `index = faiss.IndexFlatL2(dimension)`

Each chunk carries metadata including:

- `type`
- `name`
- `file_name`
- `file_path`
- `content`

This helps the assistant answer questions like where a function or variable is defined.

## Conversation Persistence

Conversation history is stored in:

```text
storage/conversation.json
```

Recent turns are included in retrieval and prompt construction so follow-up questions like "what does that function return?" can use earlier context.

## Current MVP scope

- indexing currently works on Python files
- embeddings use `text-embedding-3-small`
- answers use `gpt-4.1-mini`

## Index Options

Indexed supports two FAISS index choices:

- `flat`: exact nearest-neighbor search, simpler default
- `hnsw`: approximate nearest-neighbor search, usually faster on larger datasets

If you switch index types, rebuild the index so `storage/code.index` is recreated with the new FAISS structure.

## Reset Generated Data

To clear generated indexes, metadata, saved conversation history, and cloned repos:

```bash
python scripts/flush.py
```

This is useful when you want a clean slate before re-indexing a repository.

## Project structure

- `app/main.py`: CLI entrypoint, index selection, and Q&A loop
- `app/ingest.py`: clone repositories
- `app/utils.py`: collect code files
- `app/chunker.py`: extract Python functions and module-level assignment chunks
- `app/embedder.py`: create embeddings
- `app/indexer.py`: create, save, and load the FAISS index
- `app/retriever.py`: retrieve relevant chunks
- `app/qa.py`: generate answers from retrieved context and conversation history
- `scripts/flush.py`: clear generated storage and cloned repos
