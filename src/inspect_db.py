from retriever import retrieve_documents

question = "What is XP?"

results = retrieve_documents(question, n_results=5)

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Source:", result.source)
    print("Distance:", result.distance)
    print("Page:", result.page_number)
    print("Text:", result.text)