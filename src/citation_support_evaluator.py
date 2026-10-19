from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam

from schemas import CitationSupportReport

load_dotenv()
client = OpenAI()


def evaluate_citation_support(claim, document):
    context = (f"Source: {document.source} | "
               f"Page: {document.page_number} | "
               f"Document Text: {document.text} | "
               )

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            EasyInputMessageParam(
                role="system",
                content="""
                You evaluate whether a specific cited document supports
                a factual claim in a RAG-generated answer.
    
                Use only the supplied document text as evidence.
    
                Assign exactly one support level:
    
                - supported: The document directly supports the entire claim.
                - partially_supported: The document supports part of the claim,
                  but some details remain unsupported.
                - unsupported: The document does not provide sufficient
                  evidence for the claim.
                  
                  Rules:
                    1. Evaluate only the supplied document, not outside knowledge.
                    2. Do not use evidence from other documents.
                    3. A relevant topic or heading alone is not sufficient evidence.
                    4. Check every meaningful part of the claim.
                    5. Do not assume that two related facts establish a relationship.
                    6. Quote evidence accurately; never invent quotations.
                    7. If no relevant supporting passage exists, return an empty
                       evidence string.
                    8. Explain briefly why the evidence supports or fails to
                       support the claim.
                    9. Copy the supplied source and page number exactly.
                    10. Return exactly one evaluation for the supplied claim.
                """
            ),
            EasyInputMessageParam(
                role="user",
                content=f"""
                Claim:
                
                {claim}
                
                Cited document: 
                
                {context}
                """
            )
        ],
        text_format=CitationSupportReport
    )

    return response.output_parsed

