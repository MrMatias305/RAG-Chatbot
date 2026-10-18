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

                Your task is to identify factual claims in the generated answer
                and evaluate whether each claim is supported by the retrieved
                documents.

                Follow these rules:

                1. Evaluate the answer using only the provided documents.
                2. Break the answer into individual, meaningful factual claims.
                3. Evaluate each claim separately.
                4. Set supported to true only when the documents provide
                   sufficient evidence for the claim.
                5. Set supported to false when the claim is unsupported,
                   goes beyond the evidence, or makes an inference that the
                   documents do not establish.
                6. A claim being plausible or factually correct according to
                   outside knowledge does not make it supported.
                7. Do not treat a heading, fragment, or mere mention of a
                   topic as sufficient evidence for a more detailed claim.
                8. For supported claims, quote the relevant evidence from
                   the documents.
                9. For unsupported claims, set evidence to an empty string
                   if no passage supports the claim.
                10. Explain briefly why the evidence does or does not support
                    each claim.
                11. Do not judge citation accuracy in this evaluation.
                    Evaluate only whether the claims are supported by the
                    retrieved documents.
                12. Do not invent evidence or quotations.
                13. Evaluate the actual claims made in the answer, including
                    claims that appear in its concluding sentences.
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

