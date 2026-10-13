from vector_db import get_collection

collection = get_collection()
query = "what is an AI model?"

results = collection.query(
    query_texts=[query],
    n_results=5,
    where={'source': 'Artificial Intelligence with Microsoft Power BI.pdf'},
    include=['documents', 'metadatas', 'distances']
)

for i, document in enumerate(results['documents'][0], start=1):
    metadata = results['metadatas'][0][i-1]
    distance = results['distances'][0][i-1]

    print(f"\nSource: ", metadata['source'])
    print("Page: ", metadata['page_number'])
    print("Distance: ", distance)
    print("Text: ", document)