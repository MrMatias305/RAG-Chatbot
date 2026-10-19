from rag import generate_answer


def evaluate_citations(questions, k=3):
    answers_with_citation = 0
    total_citations = 0
    valid_citations = 0

    for question in questions:
        result, documents = generate_answer(
            question,
            n_results=k,
            collection_name='research_documents_300'
        )
        citations = result.citations

        if citations:
            answers_with_citation += 1

        retrieved_pages = {
            (document.source, document.page_number)
            for document in documents
        }

        print(f"\nQuestion: {question}")

        for citation in citations:
            total_citations += 1
            citation_key = (
                citation.source,
                citation.page_number
            )

            is_valid = citation_key in retrieved_pages
            if is_valid:
                valid_citations += 1

            print(f"Citation: {citation.source} | pp. {citation.page_number} | "
                  f"{'VALID' if is_valid else 'INVALID'}")

        if not citations:
            print(f"No citation found")

    if not questions:
        print(f"No questions found")
        return

    validity_rate = valid_citations / total_citations * 100 if total_citations else 0
    citation_coverage = answers_with_citation / len(questions) * 100

    print("="*80)
    print(f"CITATION EVALUATION RESULTS")
    print("="*80)
    print(f"Questions evaluated: {len(questions)}")
    print(f"Total citations: {total_citations}")
    print(f"Valid citations: {valid_citations}")
    print(f"Invalid citations: {total_citations - valid_citations}")
    print(f"Citation validity: {validity_rate:.2f}%")
    print(f"Citation coverage: {citation_coverage:.2f}%")
    print("="*80)



if __name__ == "__main__":
    questions = [
        "What is the relationship between AI and BI?",
        "What are the key practices of Scrum?",
        "What is the capital of France?",
        "What is the relationship between Scrum and the boiling point of water?",
    ]
    evaluate_citations(questions, 3)