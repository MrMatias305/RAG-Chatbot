from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam

from retriever import retrieve_documents
from schemas import RAGAnswer

load_dotenv()
client = OpenAI()

def generate_answer(question,
                    n_results=3,
                    collection_name="research_documents_300"):
    """Generates answer from question"""

    # Retrieve documents
    documents = retrieve_documents(question,
                                   n_results,
                                   collection_name
                                   )

    if not documents:
        return (RAGAnswer(
            answer="I cannot find relevant information in the documents",
            citations=[],
            insufficient_context=True,
        ), [])

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
                1. Use only provided context as evidence and do not use outside information to fill gaps.
                2. Every factual claim in your answer must be supported by the provided context.
                3. Do not infer details that the context do not establish.
                4. If the context only has a heading, an incomplete sentence, or a fragment of information,
                    do not treat as a sufficient evidence for a detailed claim.
                5. If the context partially supports the answer, explain what can be established and what is 
                    missing.
                6. Set insufficient_context true when the context does not adequately support a complete answer
                    to the question. Set it to false only when the context adequately support the answer.
                7. Include citations only to sources and page numbers provided in the context.
                8. Cite only sources that support claims made in your answer.
                9. If the context provides no meaningful evidence for an answer, state that the available 
                    documents do not provide sufficient information and return an empty citation list.
                10. If the context partially supports the answer, cite the supporting sources and clearly 
                    acknowledge limitations.
                 
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

    return response.output_parsed, documents

if __name__ == '__main__':
    question = input("> ")
    result, documents = generate_answer(question, 3, "research_documents_300")

    print("\n--- Answer ---")
    print(result.answer)

    if result.citations:
        print("\n--- Sources ---")
        for i, citation in enumerate(result.citations, start=1):
            print(f"[{i}] Source: {citation.source} | pp. {citation.page_number}")

    print("\nInsufficient context" if result.insufficient_context else
          "\nSufficient context reported by model")

    print("\n--- Retrieved Documents ---")
    for i, document in enumerate(documents, start=1):
        print(f"[{i}] Source: {document.source} | pp. {document.page_number} | dist. {document.distance:.3f}")
