from grounding_benchmark import benchmark_cases
from retriever import retrieve_documents


def inspect_benchmark():
    for case in benchmark_cases:
        print("="*80)
        print(f"Benchmark ID: {case["id"]}")
        print(f"Claim: {case['claim']}")
        print(f"Support level: {case['support_level']}")
        print(f"Reason: {case['reason']}")

        documents = retrieve_documents(
            case['claim'],
            n_results=3,
            collection_name="research_documents_300",
        )

        print("\nRetrieved evidence:")

        if not documents:
            continue

        for i, document in enumerate(documents, start=1):
            print(f"\nDocument {i}")
            print(f"Source: {document.source} | pp. {document.page_number} | Distance: {document.distance:.2f}")
            print(f"Text: {document.text}")


if __name__ == "__main__":
    inspect_benchmark()