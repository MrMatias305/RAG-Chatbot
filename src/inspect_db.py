from vector_db import get_collection

collection = get_collection()

print("Collection: ", collection.name)
print("Total stored chunks: ", collection.count())