from pydantic import BaseModel, Field


class RetrievedDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float= Field(ge=0)


class Citation(BaseModel):
    source: str
    page_number: int


class RAGAnswer(BaseModel):
    answer: str
    citations: list[Citation]
    insufficient_context: bool


class GroundingEvaluation(BaseModel):
    claim: str
    support_level: str
    evidence: str
    explanation: str


class GroundingReport(BaseModel):
    evaluations: list[GroundingEvaluation]


class CitationSupportEvaluation(BaseModel):
    claim: str
    source: str
    page_number: int
    support_level: str
    evidence: str
    explanation: str


class CitationSupportReport(BaseModel):
    evaluations: list[CitationSupportEvaluation]


if __name__ == '__main__':
    print(GroundingEvaluation(
        claim="AI models analyze datasets to identify patterns.",
        support_level="fully supported",
        evidence="The AI model utilizes a data set and searches through it for patterns.",
        explanation="The retrieved passage directly supports the claim.",
    ))