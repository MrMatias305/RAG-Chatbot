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
