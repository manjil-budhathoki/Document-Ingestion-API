import fitz # from PyMuPDF
from fastapi import UploadFile

def extract_text(file: UploadFile) -> str:
    """
    Extract text form a given file (PDF or TXT).

    Args:
        file (UploadFile): The uploaded file objecct from FastAPI.
    
        
    Returns:
        str: The extracted texxt content.
    
    
    Raises:
        Exception: If there's an error during processing.
    """

    extracted_text = ""

    # for text/plain files
    if file.content_type == "text/plain":
        contents = file.file.read()
        extracted_text += contents.decode("utf-8")
    

    # for application/pdf files
    elif file.content_type == "application/pdf":
        pdf_document = fitz.open(stream=file.file.read(), filetype="pdf")
        for page in pdf_document:
            extracted_text += page.get_text()
        pdf_document.close()
    
    return extracted_text

    