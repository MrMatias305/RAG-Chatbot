benchmark_cases = [
    {
        "id": "G1",
        "claim": "AI models can make decisions or predictions based on data.",
        "support_level": "supported",
        "reason": (
            "The retrieved AI document explicitly states that AI models "
            "can arrive at decisions or make predictions based on data."
        ),
    },
    {
        "id": "G2",
        "claim": "Incorrect data relationships can cause data to be omitted from analysis.",
        "support_level": "supported",
        "reason": (
            "The retrieved Power BI document explicitly describes this risk."
        ),
    },
    {
        "id": "G3",
        "claim": "AI and BI both benefit from correctly configured data relationships.",
        "support_level": "supported",
        "reason": (
            "The retrieved document identifies getting data right for AI "
            "and business intelligence as an important purpose of data relationships."
        ),
    },
    {
        "id": "G4",
        "claim": "AI extends BI by adding predictive capabilities.",
        "support_level": "unsupported",
        "reason": (
            "The retrieved passages discussed so far do not explicitly "
            "establish this particular relationship."
        ),
    },
    {
        "id": "G5",
        "claim": "BI provides the foundational data structures necessary for every AI system.",
        "support_level": "partially_supported",
        "reason": (
            "The documents support the importance of data modeling for AI "
            "and BI, but do not establish that BI provides the foundation "
            "for every AI system."
        ),
    },
]