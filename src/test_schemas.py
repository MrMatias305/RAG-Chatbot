from schemas import RetriedDocument

document = RetriedDocument(
    text="AI can help analyze business data",
    source="modern_world_with_AI_agesnts.pdf",
    page_number=24,
    distance=0.73,
)

print("Valid document: ", document.text)
print("Source: ", document.source)
print("Page number: ", document.page_number)
print("Distance: ", document.distance)