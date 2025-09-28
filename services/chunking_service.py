from enum import Enum
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from schemas.document import Chunk 

class ChunkingStrategy(str, Enum):
    RECURSIVE = "recursive"
    FIXED_SIZE = "fixed_size"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# The core logic of the splitters remains the same, they still return List[str]
def _chunk_text_recursively(text: str) -> List[str]:
   
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)

def _chunk_text_fixed_size(text: str) -> List[str]:
    
    if len(text) <= CHUNK_SIZE:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


# The main function is updated to create Chunk objects
def chunk_text(
    text: str, 
    strategy: ChunkingStrategy, 
    source_filename: str
) -> List[Chunk]:
    """
    Main function to chunk text and associate metadata with each chunk.
    """
    # get the raw text chunks from the selected strategy
    if strategy == ChunkingStrategy.RECURSIVE:
        raw_chunks = _chunk_text_recursively(text)
    elif strategy == ChunkingStrategy.FIXED_SIZE:
        raw_chunks = _chunk_text_fixed_size(text)
    else:
        raise ValueError("Invalid chunking strategy provided.")

    # create Chunk objects with metadata for each raw chunk
    processed_chunks = []
    for i, chunk_text in enumerate(raw_chunks):
        metadata = {
            "source_filename": source_filename,
            "chunk_number": i + 1,
            "total_chunks": len(raw_chunks)
        }
        processed_chunks.append(Chunk(chunk_text=chunk_text, metadata=metadata))
        
    return processed_chunks