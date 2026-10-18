from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam

from schemas import GroundingReport

load_dotenv()
client = OpenAI()

def evaluate_grounding(answer, documents):
    """Evaluate the grounding result against the provided documents"""

    if not documents:
        return GroundingReport(evaluations=[])

    context_parts = []

    for i, document in enumerate(documents, start=1):
        context_parts.append(
            f"Document {i} | Source: {document.source} | "
            f"Page: {document.page_number}\n"
            f"Document text: {document.text}"
        )

    context = "\n\n".join(context_parts)

    response = client.responses.parse(
        model="gpt-4.1-mini",
        input=[
            EasyInputMessageParam(
                role="system",
                content="""
                You are an evaluator of answer grounding in a RAG system.

                Your task is to identify factual claims in a generated answer
                and evaluate how well each claim is supported by the retrieved
                documents.

                Follow these rules:

                1. Evaluate claims using only the provided documents.
                2. Break the answer into individual, meaningful factual claims.
                3. Evaluate each claim separately, including claims in
                   concluding sentences.
                4. Assign exactly one of these support levels to each claim:

                   - "supported": The retrieved documents provide sufficient
                     evidence for the entire claim.
                   - "partially_supported": The documents support some parts
                     of the claim, but other parts are missing, unclear, or
                     unsupported.
                   - "unsupported": The documents provide no sufficient
                     evidence for the claim.

                5. A claim being plausible or factually correct according to
                   outside knowledge does not make it supported.
                6. Do not treat a heading, fragment, or mere mention of a
                   topic as sufficient evidence for a detailed claim.
                7. For "supported" claims, provide evidence that supports
                   the entire claim.
                8. For "partially_supported" claims, provide the evidence
                   supporting the claim's supported portion and explain
                   what remains unsupported.
                9. For "unsupported" claims, set evidence to an empty string
                   if no relevant supporting passage exists.
                10. Quote evidence accurately. Do not invent quotations.
                11. Explain briefly why the evidence does or does not support
                    each claim.
                12. Do not evaluate citation accuracy. Evaluate only whether
                    claims are grounded in the retrieved documents.
                13. Be strict. Do not classify an entire claim as
                    "supported" when the evidence establishes only part of it.
                14. Return one of the three exact support-level values for
                    every claim: supported, partially_supported, unsupported.
                """
            ),
            EasyInputMessageParam(
                role="system",
                content=f"""
                Retrieved documents:
                
                {context}
                
                Answer:
                
                {answer}
                
                Evaluate the factual claims in the generated answer.
                """
            )
        ],
        text_format=GroundingReport
    )

    return response.output_parsed

