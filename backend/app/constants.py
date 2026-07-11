"""
Shared constants.

Keeping the category list fixed and small (per PRD: 5-6 categories) matters for
two things downstream: it keeps the seed dataset organized, and it gives the
AI triage prompt a closed vocabulary to reason over instead of free-form tags.
"""

CATEGORIES = [
    "housing",
    "food",
    "healthcare",
    "legal",
    "childcare",
    "employment",
    "financial_assistance",
]
