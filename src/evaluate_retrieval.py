from retriever import retrieve_documents


def evaluate_retrieval(question):
    documents = retrieve_documents(question, n_results=3)
    print("="*60)
    print("Question:", question)
    print("=" * 60)

    for i, document in enumerate(documents, start=1):
        print("Source: ", document.source)
        print("Page: ", document.page_number)
        print("Distance: ", document.distance)
        print("Text: ", document.text[:500])


if __name__ == "__main__":
    test_questions = [
        "What is the relationship between AI and BI?",
        "How does Power BI help users analyze business data?",
        "What are the differences between Scrum and Kanban?",
        "What is artificial intelligence?",
    ]

    for question in test_questions:
        evaluate_retrieval(question)

