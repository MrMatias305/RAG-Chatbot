from grounding_evaluator import evaluate_grounding
from rag import generate_answer


def test_grounding():
    """Test for grounding research documents"""

    question = "What is the relationship between AI and BI?"
    answer, documents = generate_answer(question,
                    n_results=3,
                    collection_name="research_documents_300"
                    )

    report = evaluate_grounding(answer=answer.answer, documents=documents)

    print("="*60)
    print("GROUNDING EVALUATION")
    print("="*60)

    print(f"Question: {question}")
    print(f"Answer: {answer.answer}")

    for i, evaluation in enumerate(report.evaluations, start=1):
        print(f"\nEvaluation {i}")
        print(f"Claim: {evaluation.claim}")
        print(f"Supported Claim: {evaluation.supported}")
        print(f"Evidence: {evaluation.evidence}")
        print(f"Explanation: {evaluation.explanation}")

    total_claims = len(report.evaluations)
    supported_claims = sum(evaluation.supported for evaluation in report.evaluations)

    print()
    print("=" * 60)
    print(f"Total Claims evaluated: {total_claims}")
    print(f"Supported Claims: {supported_claims}")
    print("Unsupported Claims: ", total_claims - supported_claims)
    print("="*60)


if __name__ == "__main__":
    test_grounding()