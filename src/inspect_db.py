from vector_db import get_collection

collection = get_collection()

result = collection.get(
    limit=1,
    include=['documents', 'metadatas']
)

print("ID: ", result["ids"][0])
print("Metadata: ", result["metadatas"][0])
print("Text: ", result["documents"][0])
