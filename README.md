# RAG Chatbot

A Python-based Retrieval-Augmented Generation (RAG) chatbot that allows users to search their PDF documents using semantic search. The project uses ChromaDB to store document chunks and retrieve relevant passages based on the meaning of a query.

## Overview

Traditional keyword search looks for matching words. Semantic search finds passages that are conceptually related to a question, even when the wording differs.

This project explores the foundations of RAG by building a document ingestion and retrieval pipeline step by step.

### Current Features

- Extract text from PDF documents.
- Clean extracted text by normalizing whitespace.
- Split text into overlapping chunks.
- Assign sequential IDs to chunks.
- Store document text and metadata in ChromaDB.
- Generate embeddings automatically using ChromaDB's default embedding function.
- Perform semantic searches against stored documents.
- Retrieve source filenames and page numbers.
- Filter search results using metadata.
- Inspect retrieved passages and their distances.

## Architecture

The current pipeline:

```text
          PDF Documents
                |
                v
        Text Extraction
                |
                v
          Text Cleaning
                |
                v
       Text Chunking
       (300 words,
        50-word overlap)
                |
                v
       Assign Chunk IDs
                |
                v
         ChromaDB
                |
                v
       Semantic Search
                |
                v
     Relevant Text Chunks
```

The project currently focuses on document ingestion and retrieval. Generating natural-language answers with an LLM is a future development step.

## Technologies

- **Python** — Application logic and document processing.
- **pypdf** — Extracting text from PDF files.
- **ChromaDB** — Persistent vector database and semantic retrieval.
- **Embeddings** — Representing document chunks and queries as numerical vectors.
- **Git** — Version control.

## Project Structure

```text
RAG-Chatbot/
├── data/
│   ├── pdfs/           # Local PDF documents
│   └── db/             # Persistent ChromaDB database
├── src/
│   ├── __init__.py
│   ├── ingest.py       # PDF ingestion and chunking
│   ├── vector_db.py    # ChromaDB operations
│   └── inspect_db.py   # Database inspection and search tests
├── .env                # Local environment variables, if needed
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd RAG-Chatbot
```

Replace `<your-repository-url>` with your Git repository URL.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install chromadb pypdf
```

### 4. Add PDF documents

Place your own PDF documents in:

```text
data/pdfs/
```

For best results with the current implementation, use PDFs containing selectable text rather than scanned page images.

**Note:** PDF documents and the local database are excluded from version control. Add your own documents locally.

### 5. Ingest documents

Run the ingestion script:

```bash
python -m src.ingest
```

The script extracts text, cleans it, divides it into chunks, assigns IDs, and stores the chunks in ChromaDB.

### 6. Inspect the database

```bash
python -m src.inspect_db
```

The inspection script can be used to check stored records and experiment with semantic queries.

## Chunking Strategy

The current implementation uses word-based chunking with these settings:

| Parameter | Value |
|---|---:|
| Chunk size | 300 words |
| Chunk overlap | 50 words |
| Step size | 250 words |

Overlapping chunks preserve some context between consecutive chunks.

Each chunk stores metadata identifying its source document and original page number.

## ChromaDB

The project uses a persistent ChromaDB collection named:

```text
research_documents
```

The database is stored locally in:

```text
data/db/
```

Each record contains:

- **ID:** A sequential identifier, such as `chunk_0001`.
- **Document:** The extracted text of a chunk.
- **Metadata:** The source PDF filename and page number.
- **Embedding:** A numerical representation used for semantic retrieval.

ChromaDB generates embeddings automatically when documents are added without explicitly supplied embeddings.

The collection uses ChromaDB's default embedding function and distance metric unless configured otherwise.

### Important Consideration

Sequential chunk IDs are suitable for learning and experimentation, but they are not stable identifiers for document content.

When documents or chunk ordering change, existing IDs may refer to different text. The current ingestion pipeline also does not automatically remove obsolete records.

These limitations will be addressed in a future iteration.

## Example: Semantic Search

A query might look like:

```python
results = collection.query(
    query_texts=["What is artificial intelligence?"],
    n_results=3
)
```

ChromaDB embeds the query, compares it against stored embeddings, and returns the nearest matching document chunks.

The returned metadata helps identify where the retrieved information originated.

## Current Development Status

**Completed:**
- [x] Project structure and Python environment
- [x] PDF text extraction
- [x] Text cleaning
- [x] Word-based chunking with overlap
- [x] Sequential chunk ID generation
- [x] Persistent ChromaDB collection
- [x] Chunk storage and metadata
- [x] Database inspection
- [x] Semantic search
- [x] Distance inspection
- [x] Metadata filtering
- [x] Configurable number of search results

**Planned:**
- [ ] Evaluate retrieval quality using a set of test questions
- [ ] Compare different chunk sizes
- [ ] Build an LLM-powered answer generation pipeline
- [ ] Include source citations in generated answers
- [ ] Add a FastAPI endpoint
- [ ] Develop an optional web interface
- [ ] Improve document update and deletion handling
- [ ] Add automated tests

## Learning Objectives

This project is intended to develop practical understanding of:

1. Retrieval-Augmented Generation.
2. Text extraction and preprocessing.
3. Chunking strategies and context overlap.
4. Embeddings and vector similarity.
5. Persistent vector databases.
6. Semantic retrieval and metadata filtering.
7. Retrieval evaluation.
8. Grounded LLM responses and source attribution.

