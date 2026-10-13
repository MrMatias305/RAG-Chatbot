from pathlib import Path
import chromadb

PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_DIR / "data" / "db"

def get_collection(name="research_documents"):
    client = chromadb.PersistentClient(path=DB_DIR)
    collection = client.get_or_create_collection(name=name)
    return collection

if __name__ == "__main__":
    collection = get_collection()
    print(collection)