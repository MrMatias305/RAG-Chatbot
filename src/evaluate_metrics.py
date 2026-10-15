from evaluation_data import evaluation_questions
from retriever import retrieve_documents


def evaluate_retrieval(k=3):
    hits = 0
    reciprocal_ranks = []
    evaluated_questions = 0

    for item in evaluation_questions:
        question = item['question']
        relevant_sources = set(item['relevant_sources'])

        if not relevant_sources:
            print(f"Question: {question}")
            print(f"Skipped: no relevant sources found")
            continue

        evaluated_questions += 1
        documents = retrieve_documents(question, n_results=k)
        first_relevant_rank = None

        for rank, document in enumerate(documents, start=1):
            retrieved_source = (
                document.source,
                document.page_number,
            )

            if retrieved_source in relevant_sources:
                first_relevant_rank = rank
                break

        # Calculate hit and reciprocal rank
        if first_relevant_rank is not None:
            hits += 1
            reciprocal_ranks.append(1 / first_relevant_rank)
        else:
            reciprocal_ranks.append(0)

        print(f"Question: {question}")
        print(f"First relevant rank: {first_relevant_rank}")

    if evaluated_questions == 0:
        print("No questions evaluated")
        return

    hit_rate = hits / evaluated_questions
    mrr = sum(reciprocal_ranks) / evaluated_questions

    print("\n", "="*40)
    print(f"Hit Rate@{k}: {hit_rate:.2%}")
    print(f"MRR: {mrr:.4%}")
    print("="*40)

if __name__ == "__main__":
    evaluate_retrieval(3)
