from qdrant_client import QdrantClient, models
from typing import List, Dict, Any
import uuid

# The dimension of the embeddings produced by the 'all-MiniLM-L6-v2' model.
# This is crucial for setting up the Qdrant collection correctly.
VECTOR_DIMENSION = 384

QDRANT_COLLECTION_NAME = "documents_collection"

class VectorDBService:
    """
    A service for interacting with the Qdrant vector database.
    """
    def __init__(self, host: str = "localhost", port: int = 6333):
        """Initializes the Qdrant client."""
        self.client = QdrantClient(host=host, port=port)

    def upsert_vectors(
        self, 
        collection_name: str, 
        vectors: List[List[float]], 
        payloads: List[Dict[str, Any]]
    ):
    
        """
        Upserts (inserts or updates) vectors into a Qdrant collection.
        If the collection does not exist, it will be created.

        Args:
            collection_name (str): The name of the collection.
            vectors (List[List[float]]): The list of vector embeddings.
            payloads (List[Dict[str, Any]]): The list of metadata payloads for each vector.
        """
        # Ensure the collection exists, creating it if necessary.
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=VECTOR_DIMENSION, distance=models.Distance.COSINE),
        )

        # Upsert the points (vectors and payloads) in batches.
        # We generate a unique ID for each point.
        self.client.upsert(
            collection_name=collection_name,
            points=models.Batch(
                ids=[str(uuid.uuid4()) for _ in vectors],
                vectors=vectors,
                payloads=payloads
            ),
            wait=True # Wait for the operation to complete
        )
    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Searches for the most similar vectors in the collection.
        """
        search_result = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )

        return [hit.payload for hit in search_result]

# Create a single, reusable instance of the service.
vector_db_service = VectorDBService()