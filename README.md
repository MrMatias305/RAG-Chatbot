# RAG Chatbot

A Python-based **Retrieval-Augmented Generation (RAG) chatbot** that answers questions about PDF documents using semantic search and a Large Language Model (LLM).

The project combines PDF text extraction, text chunking, vector storage, semantic retrieval, context-grounded answer generation, structured responses, and source citations.

The goal is to build a practical document-question-answering application that people can run locally, experiment with, and improve. Development follows an incremental approach: establish a working application first, then improve its reliability, retrieval quality, and evaluation capabilities.

> **Project status:** The core RAG pipeline and command-line prototype are implemented. A user-friendly web interface and a community-ready release are planned.

## Overview

Traditional keyword search looks for matching words. Semantic search retrieves passages based on their conceptual similarity to a query.

Retrieval-Augmented Generation combines document retrieval with language generation. Instead of relying entirely on a language model's internal knowledge, the application retrieves relevant passages and supplies them as context for generating an answer.

This project uses ChromaDB for persistent vector storage and semantic retrieval, and the OpenAI API for answer generation.

The intended user experience is straightforward:

1. Add PDF documents to a local document collection.
2. Process and index the documents.
3. Ask questions about their contents.
4. Receive an answer generated from the retrieved context.
5. Inspect the source documents and page references.

The initial version focuses on a simple, locally runnable application rather than a complex production infrastructure.

## Features

### Implemented

**Document Processing**
- Extract text from PDFs using `pypdf`.
- Normalize extracted text.
- Split documents into overlapping, word-based chunks.
- Assign chunk identifiers.
- Preserve source filenames and page numbers as metadata.

**Vector Storage and Retrieval**
- Store document chunks in persistent ChromaDB storage.
- Generate embeddings using ChromaDB's configured embedding function.
- Retrieve semantically relevant passages.
- Configure the number of retrieved results.
- Filter retrieval by source filename.
- Inspect retrieved passages and vector distance scores.

**Answer Generation**
- Integrate retrieval with the OpenAI API.
- Generate answers using retrieved document context.
- Use the OpenAI Responses API with `gpt-4.1-mini`.
- Validate structured responses using Pydantic.
- Return source citations containing filenames and page numbers.
- Represent whether the model considers the available context insufficient.
- Handle cases where no documents are retrieved.

**Evaluation and Experimentation**
- Maintain manually labeled retrieval evaluation questions.
- Calculate Hit Rate@K, Mean Reciprocal Rank (MRR), Precision@K, and Recall@K.
- Evaluate whether retrieved context is sufficient for answering questions.
- Experiment with answer grounding and citation support.
- Inspect evaluation results to identify potential weaknesses.

### Planned

- A Streamlit web interface.
- An easier document ingestion workflow.
- A more convenient question-and-answer experience.
- Improved error handling and user feedback.
- Expanded automated testing.
- Clearer citation verification.
- Better installation and usage documentation.
- A reproducible release suitable for community use.

Features listed as planned are not necessarily available in the current implementation.

## Architecture

The current application consists of two primary pipelines.

### 1. Document Ingestion

```text
        PDF Documents
              |
              v
        Text Extraction
            (pypdf)
              |
              v
        Text Normalization
              |
              v
         Text Chunking
      (300 words, 50 overlap)
              |
              v
        Assign Chunk IDs
              |
              v
       Attach Metadata
    (source, page number)
              |
              v
           ChromaDB
              |
              v
      Persistent Storage
```

The ingestion pipeline extracts text, normalizes whitespace, divides the text into overlapping chunks, and stores the chunks and their metadata.

ChromaDB generates embeddings when documents are added without explicitly supplied embeddings.

### 2. Question Answering

```text
         User Question
               |
               v
      Semantic Retrieval
               |
               v
            ChromaDB
               |
               v
       Retrieved Passages
               |
               v
      Construct Context
               |
               v
           OpenAI API
               |
               v
       Structured Response
          /     |      \
         v      v       v
      Answer  Citations  Context
                        Status
```

The retriever finds potentially relevant passages and returns their text, source filenames, page numbers, and distance scores.

The application supplies the retrieved passages and the user's question to the language model.

The model returns a structured response containing an answer, citations, and an insufficient-context flag.

Pydantic validates the response structure. It does not independently establish the factual correctness of the answer or guarantee that every citation supports its associated claims.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and document processing |
| pypdf | PDF text extraction |
| ChromaDB | Persistent vector storage and semantic retrieval |
| Embeddings | Numerical representations used for semantic search |
| OpenAI API | Context-grounded answer generation |
| OpenAI Python SDK | Communication with the OpenAI API |
| Pydantic | Structured data validation |
| python-dotenv | Environment variable management |
| Git | Version control |
| Streamlit | Planned web interface |

## Project Structure

The project currently contains the core RAG pipeline and several development and evaluation modules.

```text
RAG-Chatbot/
├── data/
│   ├── pdfs/                       # Local PDF documents
│   └── db/                         # Persistent ChromaDB storage
├── src/
│   ├── __init__.py
│   ├── ingest.py                   # PDF ingestion and chunking
│   ├── vector_db.py                # ChromaDB management
│   ├── inspect_db.py               # Database inspection
│   ├── retriever.py                # Semantic retrieval
│   ├── test_llm.py                 # OpenAI API test
│   ├── rag.py                      # RAG answer generation
│   ├── schemas.py                  # Pydantic models
│   ├── test_schemas.py             # Schema tests
│   ├── evaluation_data.py          # Retrieval evaluation dataset
│   ├── evaluate_retrieval.py       # Retrieval inspection
│   ├── evaluate_metrics.py         # Retrieval metrics
│   ├── evaluation_answers.py       # Answer sufficiency test data
│   ├── evaluate_answers.py         # Answer sufficiency evaluation
│   ├── grounding_evaluator.py      # Grounding evaluation
│   ├── grounding_benchmark.py     # Grounding benchmark cases
│   └── ...                         # Additional evaluation scripts
├── .env                            # Local environment variables
├── .gitignore
└── README.md
```

Additional evaluation scripts may be present as development continues. This structure is illustrative rather than an exhaustive listing of every file.

The `data/pdfs/` directory holds local PDF documents, while `data/db/` holds the persistent vector database. These directories are intended to remain local and should not be committed to the public repository unless there is a deliberate reason to include specific sample data.

## Getting Started

### Prerequisites

- Python 3.10 or newer.
- An OpenAI API key.
- Internet connectivity for OpenAI API requests.
- PDF documents containing extractable text.

The project is developed on Linux, but the Python-based pipeline may also run on other operating systems with suitable dependencies.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd RAG-Chatbot
```

Replace `<your-repository-url>` with the actual repository URL.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install the principal dependencies used by the current implementation:

```bash
python -m pip install --upgrade pip
python -m pip install chromadb pypdf openai python-dotenv pydantic
```

A pinned dependency file will be added as part of the release preparation so that installations can be reproduced more consistently.

### 4. Configure the OpenAI API Key

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Replace the placeholder with your own API key.

Ensure that `.env` is included in `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
data/pdfs/
data/db/
```

Review the existing `.gitignore` before modifying it, and preserve any additional rules your project needs.

**Security:** Never commit API keys or other secrets to version control.

**Cost:** OpenAI API requests may incur charges. Check your API account's pricing and usage limits before running experiments.

### 5. Add PDF Documents

Place your PDF files in:

```text
data/pdfs/
```

The current ingestion pipeline is intended primarily for PDFs containing selectable text. Scanned documents may require OCR, which is not part of the current core workflow.

Use documents you have permission to process and share. For a public release, avoid including copyrighted documents without appropriate permission.

### 6. Ingest the Documents

Run the ingestion module:

```bash
python -m src.ingest
```

The pipeline extracts text, creates chunks, attaches metadata, and stores the records in ChromaDB.

### 7. Inspect the Database

```bash
python -m src.inspect_db
```

This script can be used to inspect stored records and experiment with retrieval.

### 8. Test the OpenAI API

```bash
python -m src.test_llm
```

This performs a standalone API test.

### 9. Ask Questions

Run the command-line RAG interface:

```bash
python -m src.rag
```

Enter a question when prompted.

The application retrieves passages from the selected ChromaDB collection and generates a structured response.

> **Note:** The exact commands and import conventions will be verified during release preparation. If a module cannot be run with `python -m`, use the execution method supported by the current implementation until the package imports are standardized.

## Current Chunking Configuration

The current implementation uses word-based chunks with overlapping text.

| Parameter | Value |
|---|---:|
| Chunk size | 300 words |
| Chunk overlap | 50 words |
| Step size | 250 words |

For example:

```text
Chunk 1: Words   1–300
Chunk 2: Words 251–550
Chunk 3: Words 501–800
```

The overlap helps preserve context across chunk boundaries.

Chunks that are too small may lose useful context. Chunks that are too large may contain unrelated information, making retrieval less precise.

The current configuration is a starting point rather than a universal optimum. Alternative chunk sizes and overlap settings can be evaluated as the application develops.

## Vector Storage and Retrieval

The project uses ChromaDB for persistent storage and semantic search.

The current development environment uses collections including:

```text
research_documents
research_documents_200
research_documents_300
```

These collections were created during development and experimentation. The collection names and their contents may differ between local installations.

The default collection used by a function depends on its configuration. Make sure the selected collection contains the documents you have ingested before running retrieval or answer generation.

### Stored Information

Each vector record contains:

- **ID:** A chunk identifier.
- **Document:** Extracted text from a PDF.
- **Metadata:** Source filename and page number.
- **Embedding:** A numerical representation used for semantic retrieval.

### Retrieval Parameters

The retriever supports:

| Parameter | Purpose |
|---|---|
| `query` | The user's question or search text |
| `n_results` | Maximum number of results requested |
| `collection_name` | The ChromaDB collection to search |
| `source` | Optional source filename filter |

The retriever returns structured document objects containing text, source, page number, and distance.

### Understanding Distance Scores

ChromaDB returns distance values based on the configured embedding-space distance metric.

For distance metrics where smaller values indicate closer matches, lower distances generally indicate greater vector similarity. The exact interpretation depends on the configured metric.

**A distance score is not a confidence percentage.** It does not directly establish whether a passage answers a question or whether the generated answer is correct.

### Current Limitations

- Chunk IDs are sequential and may change when the ingestion order changes.
- Comprehensive synchronization between source PDFs and stored records has not yet been implemented.
- Updating or removing PDFs may require explicit handling of existing records.
- Duplicate ingestion and stale chunks need further attention.
- Retrieval quality depends on the documents, chunking strategy, embedding configuration, and query.

Reliable document updates, deduplication, and deletion handling are future improvements.

## Structured Answers and Citations

The response models are defined in:

```text
src/schemas.py
```

The core answer structure contains:

| Field | Purpose |
|---|---|
| `answer` | Generated natural-language answer |
| `citations` | Source filenames and page numbers |
| `insufficient_context` | Indicates whether the model considers the context inadequate |

The application instructs the model to use retrieved passages as evidence, avoid unsupported assumptions, and acknowledge when the available context is insufficient.

When retrieval returns no documents, the application returns a predefined response indicating that relevant information could not be found.

Citations are currently generated as part of the structured model response. Independent verification of citation support is still under development.

Consequently, a citation may have a valid source and page reference without necessarily supporting every claim in the answer. This distinction is an important target for future improvements.

## Evaluation

The project includes experimental evaluation tools for assessing retrieval quality, context sufficiency, answer grounding, and citation support.

These tools help identify weaknesses in the system, but they are not prerequisites for using the basic RAG pipeline.

### Retrieval Metrics

The retrieval evaluator calculates four metrics.

**Hit Rate@K**

The proportion of evaluated questions for which at least one relevant result appears among the top K retrieved documents.

**Mean Reciprocal Rank (MRR)**

Measures how highly the first relevant result ranks. Higher values indicate that relevant results tend to appear nearer the top.

**Precision@K**

The proportion of retrieved documents that are labeled relevant.

**Recall@K**

The proportion of labeled relevant documents that are retrieved within the top K results.

The current evaluation data uses manually assigned relevance labels. Questions without relevance labels are skipped.

### Initial Retrieval Baseline

The initial four-question evaluation using 300-word chunks, 50-word overlap, and K = 3 produced:

| Metric | Result |
|---|---:|
| Hit Rate@3 | 100.00% |
| MRR | 87.50% |
| Mean Precision@3 | 91.67% |
| Mean Recall@3 | 91.67% |

These values are an initial development baseline, not a general performance guarantee. The dataset is small, and the results depend on the completeness and accuracy of the manually assigned labels.

### Additional Evaluation Work

Development has also explored:

- Answer sufficiency classification.
- Grounding evaluation against retrieved passages.
- Citation validity checks.
- Citation-support evaluation.

These evaluation components are experimental and should not be interpreted as proof that all generated answers are factually correct.

The immediate development priority is to finish the usable application. Evaluation will continue incrementally as part of improving reliability.
