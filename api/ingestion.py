from fastapi import APIRouter, UploadFile, File, HTTPException, status
from services.text_extractor import extract_text
from services.chunking_service import chunk_text, ChunkingStrategy

# APIRouter allows us to create a modular set of routes
router = APIRouter()

# Define allowed content types for our files
ALLOWED_CONTENT_TYPES = ["application/pdf", "text/plain"]

@router.post(
    "/upload",
    tags=["Document Ingestion"],
    summary="Upload, Extract, and Chunk Document",
)

def upload_and_extract_text(file: UploadFile = File(...)) -> dict:
    """
    Accepts a .pdf or .txt file, validates it, extracts the text using the 
    text_extractor service, and returns the extracted text.
    """

    # 1. Validate file type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Only PDF and TXT files are allowed.",
        )
    
    try:
        # 2. Call the service to perform text extraction
        extracted_text = extract_text(file)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the file: {str(e)}",
        )
    
    finally:
        file.file.close()
    

    # 3. Validate the text was extracted
    if not extracted_text or not extracted_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file appears to be empty or contains no extractable text."
        )
    
    # 4. Return a successful response
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "extracted_text_snippet": extracted_text[:200] + "..."
    }