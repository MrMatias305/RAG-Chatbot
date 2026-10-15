# RAG Chatbot

A Python-based **Retrieval-Augmented Generation (RAG) chatbot** that answers questions about PDF documents using semantic search and a Large Language Model (LLM).

The project combines PDF text extraction, text chunking, vector storage, semantic retrieval, context-grounded answer generation, structured output validation, source citations, and retrieval evaluation.

It is being developed incrementally, with an emphasis on understanding each component, evaluating retrieval quality, and improving reliability before introducing additional infrastructure.

## Overview

Traditional keyword search looks for matching words. Semantic search retrieves passages based on the conceptual similarity between a query and stored document chunks.

Retrieval-Augmented Generation (RAG) extends this approach by supplying retrieved information to a language model, which uses that context to generate an answer.

This project implements a local document retrieval pipeline using ChromaDB and an answer-generation pipeline using the OpenAI API.

The application processes PDF documents, stores their text chunks and embeddings, retrieves potentially relevant passages for a user's question, and generates a structured response with source citations.

## Current Features

### Document Processing
- Extract text from PDF documents using `pypdf`.
- Normalize extracted text by cleaning whitespace.
- Split text into overlapping word-based chunks.
- Assign sequential identifiers to chunks.
- Preserve source filenames and page numbers as metadata.

### Vector Storage and Retrieval
- Store document chunks in persistent ChromaDB storage.
- Generate embeddings using ChromaDB's default embedding function.
- Perform semantic searches against stored documents.
- Configure the number of retrieved chunks.
- Filter retrieval results using source metadata.
- Inspect retrieved passages and their distance scores.
- Reuse retrieval logic through a dedicated retriever function.

### Answer Generation
- Integrate the retriever with the OpenAI API.
- Generate natural-language answers using retrieved context.
- Use the OpenAI Responses API with `gpt-4.1-mini`.
- Construct prompts containing retrieved passages and source information.
- Instruct the model to acknowledge insufficient context.
- Generate structured answers using Pydantic and OpenAI Structured Outputs.
- Represent answer citations using source filenames and page numbers.
- Include an insufficient-context status in the response.

### Retrieval Evaluation
- Maintain a set of evaluation questions and manually labeled relevant documents.
- Calculate Hit Rate@K.
- Calculate Mean Reciprocal Rank (MRR).
- Calculate Precision@K.
- Calculate Recall@K.
- Skip questions without relevance labels.
- Handle cases where the retriever returns fewer documents than requested when calculating precision.

---

## Architecture

The application consists of two primary pipelines: document ingestion and question answering.

### 1. Document Ingestion

```text
             PDF Documents
                   |
                   v
            Text Extraction
                (pypdf)
                   |
                   v
              Text Cleaning
                   |
                   v
             Text Chunking
          (300 words, 50 overlap)
                   |
                   v
           Assign Sequential IDs
                   |
                   v
         Attach Source Metadata
                   |
                   v
                ChromaDB
                   |
                   v
         Persistent Vector Storage
```

The ingestion process extracts text from PDF documents, normalizes whitespace, splits the text into overlapping chunks, and stores the chunks with their metadata.

ChromaDB generates embeddings when documents are added without explicitly supplied embeddings.

### 2. Question Answering

```text
              User's Question
                     |
                     v
             Semantic Retrieval
                     |
                     v
               ChromaDB
                     |
                     v
           Retrieve Relevant Chunks
                     |
                     v
          Construct Context and Prompt
                     |
                     v
                OpenAI API
                     |
                     v
             Structured RAG Answer
                     |
            +--------+---------+
            |        |         |
            v        v         v
          Answer  Citations  Context Status
```

The retriever searches the stored document chunks and returns the requested number of results.

The application constructs a context containing the retrieved passages, source filenames, and page numbers. This context is passed to the language model alongside the user's question.

The model returns a structured answer containing:
- The generated answer.
- A list of source citations.
- A flag indicating whether the available context is insufficient.

The structured response is validated against a Pydantic model.

**Important:** Structured output validation checks the response's structure and data types. It does not independently establish that the answer is factually correct or that every citation genuinely supports the associated claims.

### 3. Retrieval Evaluation

```text
             Evaluation Questions
                     |
                     v
          Manually Labeled Documents
                     |
                     v
             Semantic Retrieval
                     |
                     v
          Compare Retrieved Results
          Against Relevance Labels
                     |
                     v
             Calculate Metrics
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Hit Rate     MRR     Precision/Recall
```

The evaluation pipeline measures how well the retriever ranks and retrieves documents that have been manually labeled as relevant to each question.

---

## Technologies

| Technology | Purpose |
|---|---|
| Python | Application logic and document processing |
| pypdf | Extracting text from PDF documents |
| ChromaDB | Persistent vector storage and semantic retrieval |
| Embeddings | Representing text as numerical vectors |
| OpenAI API | Generating answers from retrieved context |
| OpenAI Python SDK | Communicating with the OpenAI API |
| Pydantic | Validating structured data and RAG responses |
| python-dotenv | Loading environment variables |
| Git | Version control |

## Project Structure

```text
RAG-Chatbot/
├── data/
│   ├── pdfs/                    # Local PDF documents
│   └── db/                      # Persistent ChromaDB database
├── src/
│   ├── __init__.py
│   ├── ingest.py                # PDF ingestion and text chunking
│   ├── vector_db.py             # ChromaDB collection management
│   ├── inspect_db.py            # Database inspection and retrieval experiments
│   ├── retriever.py             # Reusable semantic retrieval function
│   ├── test_llm.py              # Standalone OpenAI API test
│   ├── rag.py                   # RAG answer generation
│   ├── schemas.py               # Pydantic response models
│   ├── test_schemas.py          # Schema validation tests
│   ├── evaluate_retrieval.py    # Inspect retrieved evaluation results
│   ├── evaluation_data.py       # Evaluation questions and relevance labels
│   └── evaluate_metrics.py      # Retrieval evaluation metrics
├── .env                         # Local environment variables
├── .gitignore
└── README.md
```

The `data/pdfs/` and `data/db/` directories contain local data and are intended to be excluded from version control.

The project structure above describes the current core implementation. Additional files may be present as development continues.

---

## Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd RAG-Chatbot
```

Replace `<your-repository-url>` with the repository's actual Git URL.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install chromadb pypdf openai python-dotenv pydantic
```

These commands install the principal dependencies used by the current implementation.

### 4. Configure the OpenAI API Key

Create a `.env` file in the project root and add:

```dotenv
OPENAI_API_KEY=your_actual_api_key_here
```

Replace the placeholder with your own API key.

Ensure `.env` is included in `.gitignore`:

```gitignore
.env
```

Never commit API keys or other secrets to version control.

**Note:** OpenAI API access may require billing setup, and API usage may incur charges.

### 5. Add PDF Documents

Place PDF documents inside:

```text
data/pdfs/
```

The current implementation is intended primarily for PDFs containing selectable text rather than scanned page images requiring OCR.

Documents and the persistent vector database are local application data. Users should supply their own PDFs.

### 6. Ingest Documents

Run:

```bash
python -m src.ingest
```

The ingestion pipeline extracts PDF text, normalizes whitespace, divides the text into chunks, assigns IDs, and stores the chunks and metadata in ChromaDB.

### 7. Inspect the Database

Run:

```bash
python -m src.inspect_db
```

Use this script to inspect stored records, examine retrieved passages, and experiment with semantic queries.

### 8. Test the OpenAI API Connection

Run:

```bash
python -m src.test_llm
```

This performs a standalone API request to check connectivity and answer generation.

### 9. Run the RAG Chatbot

Run:

```bash
python -m src.rag
```

Enter a question about your PDFs when prompted.

The application retrieves relevant chunks, constructs a context-aware prompt, and requests a structured answer from the OpenAI API.

### 10. Inspect Retrieval Results

Run:

```bash
python -m src.evaluate_retrieval
```

This script runs the configured evaluation questions through the retriever and displays the retrieved documents, source metadata, distance scores, and text excerpts.

Use it to inspect retrieval behavior and determine which documents should be labeled relevant.

### 11. Evaluate Retrieval Metrics

Run:

```bash
python -m src.evaluate_metrics
```

This evaluates the retriever against the manually labeled relevance data.

Questions without relevance labels are skipped so that unannotated questions are not automatically counted as retrieval failures.

The evaluator reports Hit Rate@K, MRR, Precision@K, and Recall@K.

---

## Chunking Strategy

The current implementation uses word-based chunking with overlapping sections.

| Parameter | Value |
|---|---:|
| Chunk size | 300 words |
| Chunk overlap | 50 words |
| Step size | 250 words |

The step size determines how far the chunking window advances between consecutive chunks.

For example:

```text
Chunk 1: Words   1–300
Chunk 2: Words 251–550
Chunk 3: Words 501–800
```

The overlap helps preserve context across chunk boundaries.

Each chunk carries metadata identifying its source PDF and page number.

Chunking affects retrieval because chunks that are too small may lose useful context, while chunks that are too large may contain unrelated information.

The current configuration is a starting point. Alternative chunk sizes and overlap settings have not yet been systematically compared.

---

## ChromaDB and Vector Storage

The application uses a persistent ChromaDB collection named:

```text
research_documents
```

The database is stored locally in:

```text
data/db/
```

Each stored record contains:

- **ID:** A sequential identifier such as `chunk_0001`.
- **Document:** The extracted text of a chunk.
- **Metadata:** The source PDF filename and page number.
- **Embedding:** A numerical representation used for semantic search.

When documents are added without explicitly supplied embeddings, ChromaDB uses the collection's configured embedding function to generate them.

### Semantic Retrieval

The retriever uses ChromaDB's query functionality to retrieve chunks similar to a user's question.

Example:

```python
results = collection.query(
    query_texts=["What is artificial intelligence?"],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)
```

The `n_results` parameter specifies the requested number of matching chunks.

Because ChromaDB supports multiple queries per request, results are grouped by query. For a single query, the matching documents are accessed through:

```python
results["documents"][0]
```

### Metadata Filtering

The retriever supports optional filtering by source filename.

For example:

```python
where = {"source": "example.pdf"}
```

This restricts retrieval to chunks whose source metadata matches the specified filename.

Without a filter, the retriever searches the collection without that source restriction.

### Understanding Distance Scores

ChromaDB returns distance values representing distances between query and document embeddings.

For a collection using squared L2 distance, smaller values indicate closer embeddings.

Distance is not a confidence percentage and does not directly measure answer correctness. Its interpretation also depends on the configured distance metric.

Retrieval quality must be evaluated by examining the returned passages and determining whether they are relevant to the question.

### Chunk IDs and Document Updates

The current ingestion implementation uses sequential chunk IDs.

These IDs are suitable for initial development, but they do not necessarily remain associated with the same content when documents or chunk ordering change.

The ingestion process also does not yet provide comprehensive synchronization between the PDF directory and the database. Updating or removing source documents may leave obsolete chunks in the collection unless they are explicitly handled.

Stable identifiers, deduplication, and reliable document update handling remain future improvements.

---

## The Retriever

The reusable retrieval logic is implemented in:

```text
src/retriever.py
```

The main function is:

```python
retrieve_documents(query, n_results=3)
```

The implementation also supports an optional source filter.

| Parameter | Purpose |
|---|---|
| `query` | The question or search text |
| `n_results` | Maximum number of chunks requested |
| `source` | Optional filename used to restrict retrieval |

The retriever returns structured document objects validated using Pydantic.

A retrieved document contains:

| Field | Description |
|---|---|
| `text` | The retrieved chunk's text |
| `source` | The source PDF filename |
| `page_number` | The associated page number |
| `distance` | The vector distance returned by ChromaDB |

Separating retrieval from answer generation makes the retriever reusable by evaluation scripts and future application interfaces.

---

## Structured RAG Responses

The application defines Pydantic models in:

```text
src/schemas.py
```

The core response models represent retrieved documents, citations, and generated answers.

Conceptually, the answer follows this structure:

```python
RAGAnswer(
    answer="Generated answer text",
    citations=[
        Citation(
            source="example.pdf",
            page_number=10
        )
    ],
    insufficient_context=False
)
```

The actual answer and citations depend on the question and retrieved context.

### Response Fields

| Field | Purpose |
|---|---|
| `answer` | The generated natural-language response |
| `citations` | Source filenames and page numbers supporting the answer |
| `insufficient_context` | Indicates whether the model considers the retrieved context inadequate |

The retrieved-document model also validates the text, source, page number, and distance.

Using structured models helps catch invalid response shapes and unexpected data types.

However, Pydantic validates the response structure rather than the factual truth of the answer. Citation correctness and answer faithfulness require separate evaluation.

### Answer Generation

The main RAG implementation is located in:

```text
src/rag.py
```

The `generate_answer()` function follows these steps:

1. **Retrieve:** Find potentially relevant chunks using the retriever.
2. **Construct context:** Combine the retrieved text with its source and page metadata.
3. **Construct the prompt:** Supply the context and user's question alongside instructions for grounded answering.
4. **Generate:** Request a structured response from the OpenAI API.
5. **Validate:** Parse the response using the `RAGAnswer` Pydantic model.

The application uses the `gpt-4.1-mini` model through the OpenAI Responses API.

### Insufficient Context

The model is instructed to answer using only the supplied context, avoid unsupported facts, and acknowledge when the available passages do not adequately answer the question.

If retrieval returns no documents, the application returns a predefined response indicating that relevant information could not be found.

When the model considers the context insufficient, it is instructed to return an appropriate status and avoid unsupported citations.

These safeguards help structure the intended behavior but do not guarantee that every answer is correct or that the model will always identify insufficient context accurately.

### Citations

Retrieved passages are supplied to the model with source filenames and page numbers.

The model is instructed to return citations for sources that support its answer and to use only source information provided in the context.

Citations are currently model-generated structured references. The application has not yet implemented an independent verification step that checks whether every citation supports the associated claims.

Citation validation and answer faithfulness are planned evaluation tasks.

---

## Retrieval Evaluation

Retrieval evaluation measures whether the system finds relevant document chunks for a set of test questions.

The evaluation implementation consists of:

| File | Purpose |
|---|---|
| `src/evaluation_data.py` | Stores test questions and manually labeled relevant documents |
| `src/evaluate_retrieval.py` | Displays retrieved documents for inspection |
| `src/evaluate_metrics.py` | Calculates retrieval evaluation metrics |

### Evaluation Data

Each evaluation question contains a list of relevant document references.

Conceptually:

```python
{
    "question": "What is artificial intelligence?",
    "relevant_sources": [
        ("example.pdf", 45),
        ("example.pdf", 60),
    ],
}
```

The filenames and page numbers must correspond to actual retrieved document metadata.

Relevance labels should be assigned by inspecting the document content and determining whether it is useful for answering the question.

For Recall@K to be meaningful, the labels should include the relevant documents identified for the question, not merely those already returned by the retriever.

Questions without relevance labels are skipped.

### Metrics

#### Hit Rate@K

Measures the proportion of evaluated questions for which at least one relevant document appears among the top K retrieved results.

\[
\operatorname{HitRate@K}
=
\frac{\text{Questions with a relevant result in top K}}
{\text{Evaluated questions}}
\]

#### Mean Reciprocal Rank (MRR)

Measures how highly the first relevant document ranks for each question.

\[
\operatorname{MRR}
=
\frac{1}{N}
\sum_{i=1}^{N}\frac{1}{r_i}
\]

Here, \(r_i\) is the rank of the first relevant result for question \(i\). A question with no relevant result among the retrieved documents contributes zero.

Higher MRR indicates that relevant results tend to appear closer to the top.

#### Precision@K

Measures the proportion of retrieved documents that are relevant.

\[
\operatorname{Precision@K}
=
\frac{\text{Relevant retrieved documents}}
{\text{Retrieved documents}}
\]

The implementation uses the actual number of returned documents as the denominator, allowing it to handle cases where fewer than K documents are returned.

If no documents are returned, precision is defined as zero for that question.

#### Recall@K

Measures the proportion of labeled relevant documents that are retrieved within the top K results.

\[
\operatorname{Recall@K}
=
\frac{\text{Relevant retrieved documents}}
{\text{Labeled relevant documents}}
\]

The evaluator calculates these metrics for each labeled question and reports the mean precision and mean recall across evaluated questions.

### Initial Evaluation Results

The initial four-question evaluation produced the following results:

| Metric | Result |
|---|---:|
| Hit Rate@3 | 100.00% |
| MRR | 87.50% |
| Mean Precision@3 | 91.67% |
| Mean Recall@3 | 91.67% |

These results are an initial baseline for the current test set and relevance labels.

The results suggest that the retriever found at least one labeled relevant document within the top three results for every evaluated question. The MRR result reflects the fact that the first relevant result did not always appear at rank one.

**These scores do not establish overall system reliability.** The evaluation set contains only four questions, and its results depend on the completeness and accuracy of the manually assigned relevance labels.

A larger and more diverse test set is needed before drawing broader conclusions.

### Current Evaluation Limitations

- The evaluation set is small.
- Relevance judgments are manually assigned.
- Recall depends on the completeness of the relevance labels.
- Evaluation results depend on the chosen chunking strategy and retrieval settings.
- Retrieval metrics do not measure the factual correctness of generated answers.
- Citation correctness and answer faithfulness have not yet been independently evaluated.

---

## Current Development Status

### Completed

- [x] Project structure and Python environment
- [x] PDF text extraction using `pypdf`
- [x] Text normalization and cleaning
- [x] Word-based chunking with overlap
- [x] Sequential chunk IDs
- [x] Persistent ChromaDB collection
- [x] Document storage and source metadata
- [x] Embedding generation through ChromaDB
- [x] Semantic retrieval
- [x] Metadata filtering
- [x] Configurable retrieval count
- [x] Retrieval distance inspection
- [x] Reusable retriever function
- [x] OpenAI API integration
- [x] Context-grounded answer generation
- [x] Pydantic models for retrieved documents and RAG answers
- [x] Structured answer generation through the OpenAI Responses API
- [x] Source and page citation representation
- [x] Insufficient-context status
- [x] Evaluation question dataset
- [x] Manual relevance labels for the initial evaluation set
- [x] Hit Rate@K
- [x] Mean Reciprocal Rank (MRR)
- [x] Precision@K
- [x] Recall@K
- [x] Handling fewer retrieved documents when calculating precision
- [x] Initial retrieval evaluation
- [x] Git version control and project commits

### Next Development Phase

#### A. Improve Retrieval Quality

- [ ] Expand the evaluation dataset with additional questions.
- [ ] Review and improve relevance labels.
- [ ] Record a reproducible baseline for retrieval settings.
- [ ] Compare alternative chunk sizes.
- [ ] Experiment with chunk overlap.
- [ ] Compare different values of K.
- [ ] Evaluate changes using the existing retrieval metrics.
- [ ] Investigate weak retrieval results.
- [ ] Improve chunk identifiers and document update handling.

#### B. Evaluate Answer Quality

- [ ] Create a dataset with expected answers or key facts.
- [ ] Test whether answers are supported by retrieved context.
- [ ] Evaluate answer relevance.
- [ ] Verify citation filenames and page numbers.
- [ ] Investigate citation support for individual claims.
- [ ] Test questions that cannot be answered from the document collection.
- [ ] Evaluate insufficient-context behavior.
- [ ] Add automated tests for important RAG behaviors.

#### C. Build an API

- [ ] Build a FastAPI application.
- [ ] Add a `POST /ask` endpoint.
- [ ] Validate API requests using Pydantic.
- [ ] Return structured answers and citations.
- [ ] Add error handling and appropriate HTTP status codes.
- [ ] Test endpoints using FastAPI's interactive documentation.
- [ ] Add API tests.
- [ ] Explore an optional web interface.

#### Additional Improvements

- [ ] Improve logging and error reporting.
- [ ] Manage API usage and costs.
- [ ] Add reliable document update and deletion handling.
- [ ] Improve reproducibility of retrieval experiments.
- [ ] Document evaluation methodology and experimental results.
