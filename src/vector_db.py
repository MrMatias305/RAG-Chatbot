from pathlib import Path
import chromadb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_DIR / "data" / "db"


def get_collection(name="research_documents"):
    """Create and return a Chromadb collection"""

    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(name=name)
    return collection


def store_chunks(chunks=None):
    """Store chunks into database"""

    collection = get_collection()

    if not chunks:
        print("No chunks found")
        return

    collection.upsert(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[{
            'source': chunk["source"],
            'page_number': chunk["page_number"],
        } for chunk in chunks]
    )

    print(f"Stored {len(chunks)} chunks")

