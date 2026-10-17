evaluation_cases = [
    {
        "id": "Q1",
        "question": "What is the relationship between AI and BI?",
        "collection_name": "research_documents_300",
        "expected_sufficient": True,
        "expected_topics": [
            "AI models",
            "data relationships",
            "data modeling",
        ],
        "description": "The retrieved documents should support an explanation of AI and BI data relationships.",
    },
    {
        "id": "Q2",
        "question": "According to the retrieved documents, what are the key practices of Scrum?",
        "collection_name": "research_documents_300",
        "expected_sufficient": False,
        "expected_topics": [
            "Scrum practices",
        ],
        "description": "The previously retrieved excerpts did not adequately explain the key Scrum practices.",
    },
    {
        "id": "Q3",
        "question": "What is the capital of France?",
        "collection_name": "research_documents_300",
        "expected_sufficient": False,
        "expected_topics": [
            "capital of France",
        ],
        "description": "Tests whether the chatbot avoids answering from general knowledge when its retrieved context does not support the answer.",
    },
    {
        "id": "Q4",
        "question": "What is the relationship between Scrum and the boiling point of water?",
        "collection_name": "research_documents_300",
        "expected_sufficient": False,
        "expected_topics": [
            "Scrum",
            "boiling point of water",
        ],
        "description": "Tests a question combining an Agile topic with unrelated scientific information.",
    },
]


if __name__ == "__main__":
    print("Total evaluation cases:", len(evaluation_cases))

    for case in evaluation_cases:
        print(f"Case ID: {case['id']}")
        print(f"Expected Sufficient: {case['expected_sufficient']}")
        print()