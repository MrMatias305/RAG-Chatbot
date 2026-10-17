from evaluation_answers import evaluation_cases
from rag import generate_answer


def evaluate_answers():
    total = 0
    correct = 0

    for case in evaluation_cases:
        id = case['id']
        question = case["question"]
        collection_name = case["collection_name"]
        expected_sufficient = case["expected_sufficient"]

        result = generate_answer(
            question,
            collection_name=collection_name
        )

        actual_sufficient = not result.insufficient_context
        is_correct = expected_sufficient == actual_sufficient

        total += 1
        if is_correct:
            correct += 1

        print("="*60)
        print(f"Test: {id}")
        print(f"Question: {question}")
        print(f"Collection Name: {collection_name}")
        print(f"Expected Sufficient: {expected_sufficient}")
        print(f"Actual Sufficient: {actual_sufficient}")
        print(f"Result: {'PASS' if is_correct else 'FAIL'}")
        print(f"Answer: {result.answer}")
        print(f"Citations: {result.citations}")
        print()

    if total:
        accuracy = correct / total

        print("="*60)
        print(f"Tests passed: {correct}/{total}")
        print(f"Accuracy: {accuracy}")
        print("="*60)


if __name__ == "__main__":
    evaluate_answers()