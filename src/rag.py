from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam

from retriever import retrieve_documents
from schemas import RAGAnswer

load_dotenv()
client = OpenAI()

def generate_answer(question):
    """Generates answer from question"""

    # Retrieve documents
    documents = retrieve_documents(question, n_results=3)

    if not documents:
        return RAGAnswer(
            answer="I cannot find relevant information in the documents",
            citations=[],
            insufficient_context=True,
        )

    # Build context
    context_parts = []

    for document in documents:
        source = document.source
        page = document.page_number
        text = document.text
        context_parts.append(f"[Source: {source} | Page: {page}]\n{text}")

    context = "\n\n".join(context_parts)

    # Structure answer
    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            EasyInputMessageParam(
                role="system",
                content="""
                You are a document-question answering assistant. Answer user's question based on 
                provided context.
                
                Instructions:
                1. Do not invent facts not provided by the context.
                2. If the context is insufficient to answer, explain what is missing.
                3. Set insufficient_context true when the context does not clearly answer the question, 
                    otherwise set false.
                4. Include citations to support your answer.
                5. Use only source names and page numbers provided in the context.
                6. Do not create citations for sources that do not support your answer.
                7. If the context is insufficient, return an empty citations list, 
                    unless some sources partially support the given context.
                """
            ),
            EasyInputMessageParam(
                role="user",
                content=f"""
                Context:
                {context}
                
                Question:
                {question}
                    """
            )
        ],
        text_format=RAGAnswer,
    )

    return response.output_parsed

if __name__ == '__main__':
    question = input("> ")
    result = generate_answer(question)

    print("\n--- Answer ---")
    print(result.answer)

    if result.citations:
        print("\n--- Sources ---")
        for i, citation in enumerate(result.citations, start=1):
            print(f"{i}. [Source: {citation.source} | pp. {citation.page_number}]")

    print("\nInsufficient context" if result.insufficient_context else
          "\nSufficient context reported by model")
