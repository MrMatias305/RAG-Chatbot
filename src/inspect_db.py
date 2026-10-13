from retriever import retrieve_documents

question = "What are the differences between Scrum and Kanban?"

results = retrieve_documents(question, 5)

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Source:", result["source"])
    print("Distance:", result["distance"])
    print("Page:", result["page_number"])
    print("Text:", result["text"])