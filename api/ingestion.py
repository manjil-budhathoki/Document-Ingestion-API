import hashlib
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Query
from services.text_extractor import extract_text
from services.chunking_service import chunk_text, ChunkingStrategy
from services.embedding_service import embedding_service
from services.vector_db_service import vector_db_service
from services.database_service import metadata_db_service # Import the new service

router = APIRouter()

ALLOWED_CONTENT_TYPES = ["application/pdf", "text/plain"]
QDRANT_COLLECTION_NAME = "documents_collection"

def compute_file_hash(file_content: bytes) -> str:
    """Computes the SHA256 hash of the file content."""
    return hashlib.sha256(file_content).hexdigest()


@router.post(
    "/ingest/",
    tags=["Document Inestion"],
    summary="Process and Store Document Embeddings"
)
async def process_document( # Make the function async to read file content
    strategy: ChunkingStrategy = Query(default=ChunkingStrategy.RECURSIVE),
    file: UploadFile = File(...)
) -> dict:
    # --- 1. Hashing and Duplicate Check ---
    file_contents = await file.read()
    file_hash = compute_file_hash(file_contents)

    existing_doc = metadata_db_service.find_document_by_hash(file_hash)
    if existing_doc and existing_doc.status == "success":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This document ('{existing_doc.filename}') has already been successfully ingested."
        )

    # --- 2. Initial DB Record Creation ---
    doc_id = metadata_db_service.add_document(
        filename=file.filename,
        file_hash=file_hash,
        strategy=strategy.value
    )
    
    try:
        # Reset file pointer after reading for the hash
        await file.seek(0)

        # --- 3. Text Extraction and Chunking ---
        extracted_text = extract_text(file)
        if not extracted_text or not extracted_text.strip():
            raise ValueError("Empty or non-extractable text content.")
        
        chunks = chunk_text(
            text=extracted_text,
            strategy=strategy,
            source_filename=file.filename
        )
        
        # --- 4. Embedding and Vector Storage ---
        chunk_texts = [chunk.chunk_text for chunk in chunks]
        chunk_payloads = [chunk.metadata for chunk in chunks]
        embeddings = embedding_service.generate_embeddings(chunk_texts)
        
        vector_db_service.upsert_vectors(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors=embeddings,
            payloads=chunk_payloads
        )

        # --- 5. Final DB Status Update (Success) ---
        metadata_db_service.update_document_status(
            doc_id=doc_id, status="success", chunk_count=len(chunks)
        )

    except Exception as e:
        # --- 5b. Final DB Status Update (Failure) ---
        metadata_db_service.update_document_status(doc_id=doc_id, status="failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        await file.close()

    return {
        "status": "success",
        "document_id": doc_id,
        "detail": f"Successfully processed and stored embeddings for {file.filename}.",
    }