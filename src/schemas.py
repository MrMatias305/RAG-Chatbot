from pydantic import BaseModel, Field


class RetriedDocument(BaseModel):
    text: str
    source: str
    page_number: int
    distance: float= Field(ge=0)