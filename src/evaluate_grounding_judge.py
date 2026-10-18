from grounding_benchmark import benchmark_cases
from grounding_evaluator import evaluate_grounding
from retriever import retrieve_documents


def evaluate_judge():
    total = 0
    correct = 0

    confusion = {
        'supported': {
            'supported': 0,
            'partially_supported': 0,
            'unsupported': 0,
        },
        'partially_supported': {
            'supported': 0,
            'partially_supported': 0,
            'unsupported': 0,
        },
        'unsupported': {
            'supported': 0,
            'partially_supported': 0,
            'unsupported': 0,
        }
    }

    for case in benchmark_cases:
        print("="*80)
        print(f"Benchmark ID: {case['id']}")
        print(f"Claim: {case['claim']}")

        documents = retrieve_documents(
            case['claim'],
            n_results=3,
            collection_name='research_documents_300'
        )

        report = evaluate_grounding(
            answer=case['claim'],
            documents=documents,
        )

        if not report.evaluations:
            print("No claim evaluation returned")
            continue

        evaluation = report.evaluations[0]

        expected = case['support_level']
        predicted = evaluation.support_level

        total += 1
        if expected == predicted:
            correct += 1

        confusion[expected][predicted] += 1

        print(f"Reference label: {expected}")
        print(f"Judge label: {predicted}")
        print(f"Match: {'YES' if expected == predicted else 'NO'}")

    print("\n" + "=" * 80)
    print("GROUNDING JUDGE EVALUATION")
    print("=" * 80)

    if total == 0:
        print("No benchmark cases were evaluated.")
        return

    accuracy = correct / total * 100

    print(f"Cases evaluated: {total}")
    print(f"Correct labels: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")

    labels = ['supported', 'partially_supported', 'unsupported']

    print("\nCONFUSION MATRIX")
    print(f"Rows = reference labels | Columns = judge labels")
    print(f"\n{'Reference':<22}", end="")

    for label in labels:
        print(f"{label:<23}", end="")
    print()

    for expected in labels:
        print(f"{expected:<22}", end="")

        for predicted in labels:
            print(f"{confusion[expected][predicted]:<23}", end="")

        print()
    print("="*80)

if __name__ == "__main__":
    evaluate_judge()




