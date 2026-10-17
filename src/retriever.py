from schemas import RetrievedDocument
from vector_db import get_collection


def retrieve_documents(query,
                       n_results=3,
                       collection_name='research_documents',
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
    results = retrieve_documents("What is Kanban?", 5,
                                 collection_name='research_documents_200')

    for i, result in enumerate(results, start=1):
        print(f"{i}. {result.text}")
