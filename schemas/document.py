from pydantic import BaseModel
from typing import Dict, Any

class Chunk(BaseModel):
    """
    A Pydantic model representing a single text chunk with its metadata.
    """
    chunk_text: str
    metadata: Dict[str, Any]

    class Config:
        # This allows the model to be created from arbitrary class instances
        from_attributes = True