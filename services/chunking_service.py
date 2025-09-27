from enum import Enum
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

# use an Enum for clear, validated strategy selection.

class ChunkingStrategy(str, Enum):
    """
    Enum for the available chunking strategies.
    """
    RECURSIVE = "recursive"
    FIXED_SIZE = "fixed_size"

# Define Constants for chunking parameters for easy configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

def _chunk_text_recursively(text: str) -> List[str]:
    """
    Chunks text using the RecursiveCharacterTextSplitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)

def _chunk_text_fixed_size(text: str) -> List[str]:
    """
    A simple custom implementation of fixed-size chunking with overlap.
    """
    if len(text) <= CHUNK_SIZE:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def chunk_text(text: str, strategy: ChunkingStrategy) -> List[str]:
    """
    Main function to chunk text based on the selected strategy.
    This acts as a dispatcher to the actual implementation.

    Args:
        text (str): The text content to be chunked.
        strategy (ChunkingStrategy): The strategy to use for chunking.

    Returns:
        List[str]: A list of text chunks.
    """
    if strategy == ChunkingStrategy.RECURSIVE:
        return _chunk_text_recursively(text)
    elif strategy == ChunkingStrategy.FIXED_SIZE:
        return _chunk_text_fixed_size(text)
    else:
        # This case should ideally not be hit if using the Enum correctly
        raise ValueError("Invalid chunking strategy provided.")