from pydantic import ValidationError

from schemas import RetrievedDocument

document = RetrievedDocument(
    text="AI can help analyze business data",
    source="modern_world_with_AI_agesnts.pdf",
    page_number=24,
    distance=0.73,
)

print("Valid document: ", document.text)
print("Source: ", document.source)
print("Page number: ", document.page_number)
print("Distance: ", document.distance)

print("\nChecking invalid document...")
try:
    RetrievedDocument(
        text="AI can help analyze business data",
        source="modern_world_with_AI_agesnts.pdf",
        page_number="not a page",
        distance=-0.48,
    )
except ValidationError as e:
    print(e)