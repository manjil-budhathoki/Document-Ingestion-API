from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.query_service import process_query
from services.intent_service import detect_booking_intent
from services.database_service import metadata_db_service

router = APIRouter()

class UserQuery(BaseModel):
    """Pydantic model for the user's query."""
    question: str
    session_id: str

class QueryResponse(BaseModel):
    """Pydantic model for the response."""
    answer: str

    action_required: str = "none" # "none" or "book_interview"

class BookingDetails(BaseModel):
    name: str
    email: str
    date: str
    time: str


@router.post(
    "/query/",
    tags=["Conversational RAG"],
    summary="Ask a question to the RAG system",
    response_model=QueryResponse
)
def handle_conversation(query: UserQuery) -> QueryResponse:
    """
    Handles the main conversation flow. Detects user intent and either
    triggers the RAG pipeline or signals for an interview booking.
    """
    # --- 1. INTENT DETECTION STEP ---
    is_booking_intent = detect_booking_intent(query.question)
    
    if is_booking_intent:
        # If intent is to book, send a specific response
        return QueryResponse(
            answer="It looks like you want to book an interview. Please provide your name, email, and preferred date and time.",
            action_required="book_interview"
        )
    
    # --- 2. RAG PIPELINE (if no booking intent) ---
    try:
        answer = process_query(query.question, query.session_id)
        return QueryResponse(answer=answer)
    except Exception as e:
        print(f"Error during query processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the query."
        )

@router.post(
    "/book-interview/",
    tags=["Conversational RAG"],
    summary="Saves interview booking details to the database"
)

def book_interview(details: BookingDetails) -> dict:
    """
    Receives booking details and saves them to the database.
    """
    try:
        booking_id = metadata_db_service.add_booking(
            name=details.name,
            email=details.email,
            date=details.date,
            time=details.time
        )
        return {
            "status": "success",
            "message": f"Interview booked successfully! Your booking ID is {booking_id}.",
            "booking_id": booking_id
        }
    except Exception as e:
        print(f"Error saving booking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save booking details."
        )