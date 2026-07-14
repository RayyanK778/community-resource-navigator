"""
Shared constants.

Keeping the category list fixed and small (7 categories, per PRD) matters for
two things downstream: it keeps the seed dataset organized, and it gives the
AI triage prompt a closed vocabulary to reason over instead of free-form tags.

Values are stored as stable snake_case (safe as DB values, URL query params,
and dict keys). CATEGORY_LABELS maps each to the human-readable form for
display in the UI.
"""

CATEGORIES = [
    "housing",
    "food",
    "healthcare",
    "employment",
    "childcare",
    "financial_assistance",
    "legal",
]

CATEGORY_LABELS = {
    "housing": "Housing",
    "food": "Food",
    "healthcare": "Healthcare",
    "employment": "Employment",
    "childcare": "Childcare",
    "financial_assistance": "Financial Assistance",
    "legal": "Legal",
}

