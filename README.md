# Indexed

Indexed is a lightweight codebase Q&A tool built with retrieval-augmented generation. It clones a repository, indexes Python code into FAISS or Chroma, and answers questions using retrieved code context plus conversation history.

## Features

- Clone and index a GitHub repository locally
- Parse Python code with `ast`
- Index top-level functions and module-level assignments
- Store chunk metadata including symbol name, file name, and file path
- Retrieve relevant chunks with FAISS or Chroma
- Support both `flat` and `hnsw` FAISS index types
- Let users choose between a FAISS index and a Chroma collection
- Persist conversation history for follow-up questions
- Reset generated state with a simple flush script

## How It Works

1. The repository is cloned into `repos/`.
2. Supported code files are collected from the cloned project.
3. Python files are chunked into retrievable units.
4. Chunks are embedded with OpenAI embeddings.
5. Embeddings and metadata are stored in the selected vector backend.
6. User questions retrieve the most relevant chunks.
7. Retrieved code context and recent conversation history are sent to the chat model for answering.

## Architecture

```text
+--------------------+
| User / CLI         |
| app/main.py        |
+---------+----------+
          |
          v
+--------------------+
| Repo ingestion     |
| ingest.py          |
| utils.py           |
+---------+----------+
          |
          v
+--------------------+
| Chunk extraction   |
| chunker.py         |
+---------+----------+
          |
          v
+--------------------+
| Embeddings         |
| embedder.py        |
| OpenAI API         |
+---------+----------+
          |
          v
+--------------------+
| Vector store layer |
| vector_store.py    |
+----+----------+----+
     |          |
     v          v
+---------+  +----------------+
| FAISS   |  | Chroma         |
|indexer.py| | db.py          |
|code.index| | storage/chroma |
|metadata  | | collection     |
+----+----+  +--------+-------+
     |                |
     +--------+-------+
              |
              v
+--------------------+
| Retrieval          |
| retriever.py       |
+---------+----------+
          |
          v
+--------------------+
| QA + history       |
| qa.py              |
| conversation.json  |
+---------+----------+
          |
          v
+--------------------+
| Final answer       |
+--------------------+
```

## Requirements

- Python 3.10+
- An OpenAI API key

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the CLI from the project root:

```bash
python app/main.py
```

You will be prompted for:

- a GitHub repository URL
- a vector backend: `faiss` or `chroma`
- a FAISS index type: `flat` or `hnsw` when `faiss` is selected
- follow-up questions about the indexed repository

CLI commands:

- `exit` ends the session
- `clear` clears saved conversation history

Pressing Enter at the backend prompt uses `faiss`. Pressing Enter at the FAISS index prompt uses the default index type: `flat`.

## Indexed Data

For Python files, Indexed currently stores:

- top-level functions
- module-level constants
- other module-level assignments

Each chunk includes:

- `type`
- `name`
- `file_name`
- `file_path`
- `content`

This metadata helps the assistant answer location-based questions such as where a function or variable is defined.

## Conversation History

Conversation history is stored in:

```text
storage/conversation.json
```

Recent turns are reused during retrieval and answer generation so follow-up questions can stay grounded in earlier context.

## Index Types

Indexed supports two vector backends:

- `faiss` for local vector search with `flat` and `hnsw` index types
- `chroma` for local persistent vector storage and retrieval

FAISS supports:

- `flat` for exact nearest-neighbor search
- `hnsw` for approximate nearest-neighbor search with better scalability on larger datasets

If you switch vector backends or FAISS index types, rebuild the index so the stored data matches the selected backend.

## Resetting Generated Data

To remove generated indexes, metadata, conversation history, and cloned repositories:

```bash
python scripts/flush.py
```

## Project Structure

- `app/main.py`: CLI entrypoint and indexing flow
- `app/ingest.py`: repository cloning
- `app/utils.py`: code file discovery
- `app/chunker.py`: Python chunk extraction
- `app/embedder.py`: embedding generation
- `app/indexer.py`: FAISS index creation, loading, and persistence
- `app/db.py`: Chroma client and collection access
- `app/vector_store.py`: backend selection and shared vector operations
- `app/retriever.py`: similarity search over indexed chunks
- `app/qa.py`: answer generation with retrieved context and conversation history
- `scripts/flush.py`: cleanup for generated storage and cloned repos

## Limitations

- Indexing currently focuses on Python chunk extraction
- Answer quality depends on retrieval quality and available code context
- Switching vector backend or FAISS index structure requires rebuilding the stored index

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
