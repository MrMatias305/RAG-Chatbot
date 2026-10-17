from pathlib import Path
import chromadb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_DIR / "data" / "db"


def get_collection(name="research_documents"):
    """Create and return a Chroma db collection"""

    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(name=name)
    return collection


def store_chunks(chunks=None, collection_name='research_documents'):
    """Store chunks into database"""

    collection = get_collection(collection_name)

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


if __name__ == "__main__":
    collection = get_collection('research_documents_200')
    results = collection.get(include=["documents"])

    word_counts = [len(document.split()) for document in results["documents"]]

    print("Collection: ", collection.name)
    print("Total chunks: ", len(word_counts))
    print("Minimum word count: ", min(word_counts, default=0))
    print("Maximum word count: ", max(word_counts, default=0))
    print("Chunks exceeding 300 counts: ", sum(n > 300 for n in word_counts))
    print("Chunks with 50 or fewer counts: ", sum(n <= 50 for n in word_counts))
    print("Empty chunks: ", sum(n == 0 for n in word_counts))


