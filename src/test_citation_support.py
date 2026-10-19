from citation_support_evaluator import evaluate_citation_support
from retriever import retrieve_documents


def test_citation_support():
    claim = "The boiling point of water is 100 degrees Celsius at standard atmospheric pressure."

    documents = retrieve_documents(
        claim,
        n_results=3,
        collection_name="research_documents_300"
    )

    if not documents:
        print("No documents retrieved")
        return

    document = documents[0]

    print("="*80)
    print("CITATION SUPPORT TEST")
    print("=" * 80)

    print("Claim: ", claim)
    print(f"Source: {document.source}")
    print(f"Page: {document.page_number}")

    report = evaluate_citation_support(claim, document)

    if not report.evaluations:
        print("No evaluations found")
        return

    evaluation = report.evaluations[0]

    print(f"Support level: {evaluation.support_level}")
    print(f"Evidence: {evaluation.evidence}")
    print(f"Explanation: {evaluation.explanation}")
    print("="*80)


if __name__ == "__main__":
    test_citation_support()

