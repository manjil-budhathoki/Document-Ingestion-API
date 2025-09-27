from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:
    """
    A service for generating text embeddings using a sentence-transformer model.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the EmbeddingService and loads the model.
        Loading the model is a one-time cost.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of text chunks.

        Args:
            texts (List[str]): A list of text strings to be embedded.

        Returns:
            List[List[float]]: A list of vector embeddings.
        """
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()

# Create a single, reusable instance of the service.
# The model will be loaded into memory only once when the application starts.
embedding_service = EmbeddingService()