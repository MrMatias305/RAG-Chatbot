from evaluation_answers import evaluation_cases
from rag import generate_answer


def evaluate_answers():
    total = 0
    correct = 0

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for case in evaluation_cases:
        id = case['id']
        question = case["question"]
        collection_name = case["collection_name"]
        expected_sufficient = case["expected_sufficient"]

        result, documents = generate_answer(
            question,
            collection_name=collection_name
        )

        actual_sufficient = not result.insufficient_context
        is_correct = expected_sufficient == actual_sufficient

        total += 1
        if is_correct:
            correct += 1

        # Calculate classification metrics
        if expected_sufficient and actual_sufficient:
            true_positive += 1
        elif expected_sufficient and not actual_sufficient:
            false_positive += 1
        elif not expected_sufficient and actual_sufficient:
            false_negative += 1
        else:
            true_negative += 1

        print("="*60)
        print(f"Test: {id}")
        print(f"Question: {question}")
        print(f"Collection Name: {collection_name}")
        print(f"Expected Sufficient: {expected_sufficient}")
        print(f"Actual Sufficient: {actual_sufficient}")
        print(f"Result: {'PASS' if is_correct else 'FAIL'}")
        print(f"Answer: {result.answer}")
        print(f"Citations: {result.citations}")

        print("\n--- Retrieved documents ---")
        for i, document in enumerate(documents, start=1):
            print(f"Document {i}: {document.text}")
            print(f"Source: {document.source} | pp. {document.page_number} | dist. {document.distance}")
            print()

    if total == 0:
        print("No evaluation cases found")
        return

    accuracy = correct / total
    precision = (true_positive / (true_positive + false_positive)) if true_positive + false_positive else 0
    recall = (true_positive / (true_positive + false_negative)) if true_positive + false_negative else 0
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else 0


    print("="*60)
    print("ANSWER SUFFICIENCY EVALUATION")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1 score: {f1:.2%}")
    print()
    print("CONFUSION MATRIX")
    print(f"True Positive: {true_positive}")
    print(f"False Positive: {false_positive}")
    print(f"False Negative: {false_negative}")
    print(f"True Negative: {true_negative}")
    print("="*60)


if __name__ == "__main__":
    evaluate_answers()