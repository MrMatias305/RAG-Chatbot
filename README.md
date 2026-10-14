# RAG Chatbot

A Python-based Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about their PDF documents. The project combines semantic search with a Large Language Model (LLM) to retrieve relevant passages and generate answers grounded in the retrieved context.

The project is being developed incrementally to explore document processing, vector databases, semantic retrieval, prompt construction, and LLM integration.

## Overview

Traditional keyword search looks for matching words. Semantic search retrieves passages based on the conceptual similarity between a query and stored document chunks.

Retrieval-Augmented Generation (RAG) extends semantic search by providing retrieved information to a language model, which uses that context to formulate an answer.

This project implements a basic RAG pipeline using ChromaDB for retrieval and the OpenAI API for answer generation.

### Current Features

- Extract text from PDF documents using `pypdf`.
- Clean extracted text by normalizing whitespace.
- Split text into overlapping chunks.
- Assign sequential IDs to chunks.
- Store document chunks and metadata in persistent ChromaDB storage.
- Generate embeddings using ChromaDB's default embedding function.
- Perform semantic searches against stored documents.
- Retrieve source filenames and page numbers.
- Filter search results using metadata.
- Configure the number of retrieved chunks.
- Inspect retrieved passages and their distance scores.
- Reuse retrieval logic through a dedicated retriever function.
- Connect the retriever to the OpenAI API.
- Generate natural-language answers using retrieved document context.
- Instruct the LLM to acknowledge when the provided context is insufficient.

## Architecture

The current pipeline consists of two main stages: document ingestion and question answering.

### 1. Document Ingestion

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
          (300 words, 50-word overlap)
                   |
                   v
           Assign Sequential IDs
                   |
                   v
                ChromaDB
                   |
                   v
          Persistent Vector Storage
```

### 2. Question Answering

```text
             User's Question
                    |
                    v
            Semantic Retrieval
                    |
                    v
          ChromaDB Retriever
                    |
                    v
          Retrieve Relevant Chunks
                    |
                    v
          Construct Context Prompt
                    |
                    v
              OpenAI API
                    |
                    v
             Language Model
                    |
                    v
             Generated Answer
```

The retriever searches the stored document chunks and returns the most relevant results. The application combines their text with the user's question and sends the resulting prompt to the language model.

The model is instructed to answer using the provided context and to acknowledge when that context does not contain sufficient information.

The current implementation is a basic RAG pipeline. It does not yet provide verified source citations or guarantee that every generated claim is supported by the retrieved passages.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Application logic and document processing |
| pypdf | Extracting text from PDF documents |
| ChromaDB | Persistent vector storage and semantic retrieval |
| Embeddings | Representing text as numerical vectors for similarity search |
| OpenAI API | Generating answers from retrieved context |
| OpenAI Python SDK | Communicating with the OpenAI API |
| python-dotenv | Loading environment variables from a `.env` file |
| Git | Version control |

## Project Structure

```text
RAG-Chatbot/
├── data/
│   ├── pdfs/               # Local PDF documents
│   └── db/                 # Persistent ChromaDB database
├── src/
│   ├── __init__.py
│   ├── ingest.py           # PDF extraction, cleaning, and chunking
│   ├── vector_db.py        # ChromaDB collection and storage operations
│   ├── inspect_db.py       # Database inspection and retrieval experiments
│   ├── retriever.py        # Reusable semantic retrieval function
│   ├── test_llm.py         # Standalone OpenAI API test
│   └── rag.py              # RAG pipeline and answer generation
├── .env                    # Local environment variables; never commit
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

Activate the environment on Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install chromadb pypdf openai python-dotenv
```

### 4. Configure the OpenAI API key

Create a `.env` file in the project root if one does not already exist.

Add your API key:

```dotenv
OPENAI_API_KEY=your_actual_api_key_here
```

Replace the placeholder with your actual API key.

Ensure that `.env` is included in `.gitignore`:

```gitignore
.env
```

Never commit API keys or other secrets to version control.

**Note:** Access to the OpenAI API may require billing setup, and API usage may incur charges.

### 5. Add PDF documents

Place your PDF documents inside:

```text
data/pdfs/
```

The current implementation works best with PDFs containing selectable text rather than scanned page images.

PDF documents and the persistent database are excluded from version control. Add your own documents locally.

### 6. Ingest documents

Run:

```bash
python -m src.ingest
```

The ingestion pipeline extracts text from the PDFs, normalizes whitespace, divides the text into chunks, assigns IDs, and stores the chunks and metadata in ChromaDB.

### 7. Inspect the database

Run:

```bash
python -m src.inspect_db
```

Use the inspection script to examine stored records, experiment with queries, and evaluate the retrieved passages.

### 8. Test the OpenAI API connection

Run:

```bash
python -m src.test_llm
```

This script makes a standalone API request to verify that the application can communicate with the configured language model.

### 9. Run the RAG chatbot

Run:

```bash
python -m src.rag
```

Enter a question about the contents of your PDFs when prompted.

The application retrieves relevant chunks from ChromaDB and passes their text, together with the question, to the OpenAI API for answer generation.

## Chunking Strategy

The current implementation uses word-based chunking with overlapping sections.

| Parameter | Value |
|---|---:|
| Chunk size | 300 words |
| Chunk overlap | 50 words |
| Step size | 250 words |

The overlap preserves some context between consecutive chunks.

Each chunk includes metadata identifying its source PDF and original page number.

Chunk size and overlap are configurable in the chunking function. Their effect on retrieval quality has not yet been systematically evaluated.

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

ChromaDB automatically generates embeddings when documents are added without explicitly supplied embeddings.

The collection uses ChromaDB's default embedding function and distance metric unless configured otherwise.

### Semantic Retrieval

The retriever uses ChromaDB's query functionality to find chunks similar to the user's question.

A basic query looks like this:

```python
results = collection.query(
    query_texts=["What is artificial intelligence?"],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)
```

The `n_results` parameter controls how many matching chunks are requested.

Because ChromaDB supports multiple queries in a single request, the results are grouped by query. When submitting one query, the matching chunks are accessed through:

```python
results["documents"][0]
```

### Metadata Filtering

The retriever can optionally restrict its search to a particular source document.

Conceptually, the filter is:

```python
where = {"source": "example.pdf"}
```

This restricts retrieval to chunks whose source metadata matches the specified filename.

Without a filter, the retriever searches the entire collection.

### Understanding Distance Scores

ChromaDB returns distance values that indicate the distance between the query embedding and retrieved document embeddings.

For the collection's default squared L2 distance metric, smaller values indicate closer embeddings.

However, distance is not a percentage or a direct measure of answer correctness. Retrieval quality must be evaluated by inspecting the returned content and determining whether it helps answer the question.

### Important Consideration: Chunk IDs

The current implementation uses sequential chunk IDs.

These IDs are suitable for learning and experimentation, but they are not stable identifiers for document content. If documents change or chunk ordering changes, the same ID may refer to different text.

The ingestion pipeline also does not automatically remove obsolete records. Consequently, document updates may leave stale chunks in the collection.

Stable IDs and document update handling are future improvements.

## The Retriever

The reusable retriever is implemented in:

```text
src/retriever.py
```

Its main function is:

```python
retrieve_documents(query, n_results=3, source=None)
```

Parameters:

| Parameter | Purpose |
|---|---|
| `query` | The user's question or search text |
| `n_results` | Maximum number of matching chunks to retrieve |
| `source` | Optional source filename for metadata filtering |

The function returns a list of dictionaries containing the retrieved text, source filename, page number, and distance score.

This separates retrieval logic from answer generation and allows other components to reuse the retriever.

## RAG Answer Generation

The main RAG implementation is located in:

```text
src/rag.py
```

The `generate_answer()` function follows four steps:

1. **Retrieve:** Call the retriever to find relevant chunks.
2. **Construct context:** Combine the retrieved chunk text into a context string.
3. **Construct the prompt:** Provide the context and question to the language model, along with instructions for answering.
4. **Generate:** Send the prompt to the OpenAI API and return the generated text.

Conceptually:

```python
documents = retrieve_documents(question, n_results=3)

context = "\n\n".join(
    document["text"] for document in documents
)
```

The resulting context is included in the prompt sent to the language model.

The current implementation uses the `gpt-4.1-mini` model through the OpenAI Responses API.

### Context-Grounded Answers

The prompt instructs the language model to answer using the supplied context. If the retrieved passages do not contain sufficient information, the model is instructed to say that it cannot answer based on the provided documents.

This behavior is useful for reducing unsupported answers, but prompt instructions alone cannot guarantee factual accuracy or prevent hallucinations.

The current implementation also does not yet verify individual claims against their source passages.

### Example Interaction

**Question:**

```text
How does AI assist in improving BI?
```

**Possible response:**

```text
The provided context does not explicitly explain how AI assists
in improving Business Intelligence (BI). It discusses Power BI
as a business analytics service and highlights challenges in
data preparation and access for BI but does not detail the role
of AI in enhancing BI capabilities.

Therefore, based on the provided documents, I cannot answer
how AI assists in improving BI.
```

This example illustrates the importance of retrieval quality. The chatbot may correctly recognize that its retrieved context does not contain enough information to answer the question.

However, an answer like this does not necessarily mean the entire document collection lacks the information. The retriever may simply have failed to retrieve the most useful passages.

## Current Development Status

### Completed

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
- [x] Reusable document retriever
- [x] OpenAI API connection
- [x] Basic LLM answer generation
- [x] Initial RAG pipeline combining retrieval and generation

### Planned Improvements

- [ ] Create a test set of questions with expected source passages.
- [ ] Evaluate retrieval relevance and ranking quality.
- [ ] Compare chunk sizes and overlap settings.
- [ ] Improve chunk IDs and document update handling.
- [ ] Introduce Pydantic models for structured application data.
- [ ] Explore OpenAI Structured Outputs where appropriate.
- [ ] Improve prompt construction and context handling.
- [ ] Add source citations to generated answers.
- [ ] Evaluate whether generated answers are supported by retrieved passages.
- [ ] Add automated tests.
- [ ] Build a FastAPI endpoint.
- [ ] Develop an optional web interface.
- [ ] Improve error handling, logging, and API usage management.

## Learning Objectives

This project is intended to build practical understanding of:

- PDF text extraction and preprocessing.
- Chunking strategies for retrieval systems.
- Vector databases and embeddings.
- Semantic similarity search.
- Metadata filtering.
- Retrieval quality evaluation.
- LLM integration through an API.
- Context construction and prompt engineering.
- Structured data validation.
- Reliable RAG application design.

## Future Direction

The next stage of development will focus on improving the reliability and maintainability of the current implementation before introducing additional infrastructure.

Planned improvements include retrieval evaluation, structured data models, source-aware answers, automated testing, and an API layer.

The long-term goal is to build a maintainable document question-answering application that can retrieve relevant information from a collection of PDFs and produce useful, context-grounded responses.