from typing import List

BOOKING_KEYWORDS = ["book", "interview", "schedule", "meeting", "appointment"]

def detect_booking_intent(query: str) -> bool:
    """
    Detects if the user's query is related to booking an interview.
    """
    # Simple check if any of the keywords are in the lowercased query
    return any(keyword in query.lower() for keyword in BOOKING_KEYWORDS)
