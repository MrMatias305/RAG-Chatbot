from evaluation_data import evaluation_questions
from retriever import retrieve_documents


def evaluate_retrieval(k=3):
    hits = 0
    reciprocal_ranks = []
    precision_scores = []
    recall_scores = []
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
        retrieved_sources = {
            (document.source, document.page_number) for document in documents
        }
        relevant_retrieved_sources = relevant_sources & retrieved_sources

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

        # Calculate precision
        precision = len(relevant_retrieved_sources) / k
        precision_scores.append(precision)

        # Calculate recall
        recall = len(relevant_retrieved_sources) / len(relevant_sources)
        recall_scores.append(recall)

        print(f"\nQuestion: {question}")
        print(f"First relevant rank: {first_relevant_rank}")
        print(f"Precision@{k}: {precision:.2%}")
        print(f"Recall@{k}: {recall:.2%}")

    if evaluated_questions == 0:
        print("No questions evaluated")
        return

    hit_rate = hits / evaluated_questions
    mrr = sum(reciprocal_ranks) / evaluated_questions
    mean_precision = sum(precision_scores) / evaluated_questions
    mean_recall = sum(recall_scores) / evaluated_questions

    print("\n", "="*40)
    print(f"Hit Rate@{k}: {hit_rate:.2%}")
    print(f"MRR: {mrr:.4%}")
    print(f"Mean_Precision@{k}: {mean_precision:.2%}")
    print(f"Mean_Recall@{k}: {mean_recall:.2%}")
    print("="*40)

if __name__ == "__main__":
    evaluate_retrieval(3)
