from dotenv import load_dotenv
from openai import OpenAI

from retriever import retrieve_documents

load_dotenv()
client = OpenAI()

def generate_answer(question):
    """Generates answer from question"""

    documents = retrieve_documents(question, n_results=3)

    if not documents:
        return "I cannot find relevant information in the documents"

    context = "\n\n".join(
        document["text"]
        for document in documents
    )

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

    return response.output_text

if __name__ == '__main__':
    question = input("> ")
    answer = generate_answer(question)
    print(answer)