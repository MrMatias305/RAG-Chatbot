from schemas import RetrievedDocument
from vector_db import get_collection


def retrieve_documents(query,
                       n_results=3,
                       collection_name='research_documents_300',
                       source=None):
    """Retrieves documents from a query."""

    collection = get_collection(collection_name)

    query_options = {
        'query_texts': [query],
        'n_results': n_results,
        'include': ['documents', 'metadatas', 'distances'],
    }

    if source:
        query_options['where'] = {'source': source}

    results = collection.query(**query_options)

    retrieved_documents = []

    for i, document in enumerate(results['documents'][0]):
        metadata = results['metadatas'][0][i]
        distances = results['distances'][0][i]

        retrieved_documents.append(
            RetrievedDocument(
                text=document,
                source=metadata["source"],
                page_number=metadata["page_number"],
                distance=distances,
            )
        )
    return retrieved_documents


if __name__ == "__main__":
    question = input("> ")
    documents = retrieve_documents(question,
                                   n_results=3,
                                   collection_name='research_documents_300')

    for i, document in enumerate(documents, start=1):
        print("="*60)
        print(f"DOCUMENT {i}")
        print(f"SOURCE: {document.source}")
        print(f"PAGE: {document.page_number}")
        print(f"DISTANCE: {document.distance}")
        print("=" * 60)
        print(document.text)
        print()


