from dotenv import load_dotenv
from openai import OpenAI

from retriever import retrieve_documents

load_dotenv()
client = OpenAI()

def generate_answer(question):
    """Generates answer from question"""

    # Retrieve documents
    documents = retrieve_documents(question, n_results=3)

    if not documents:
        return "I cannot find relevant information in the documents"

    # Build context
    context_parts = []

    for document in documents:
        source = document.source
        page = document.page_number
        text = document.text
        context_parts.append(f"[Source: {source} | Page: {page}]\n{text}")

    context = "\n\n".join(context_parts)

    # Construct the prompt
    prompt = f"""
    Answer the question on provided context.
    
    If the context doesn't provide enough information to answer the question, 
    say that you cannot answer based on provided documents.
    
    Context: 
    {context}
    
    Question: 
    {question}
    
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text, documents

if __name__ == '__main__':
    question = input("> ")
    answer, documents = generate_answer(question)

    print("\n--- Answer ---")
    print(answer)

    print("\n--- Sources ---")
    for i, document in enumerate(documents, start=1):
        source = document.source
        page = document.page_number
        print(f"{i}. [Source: {source} | Page: {page}]")