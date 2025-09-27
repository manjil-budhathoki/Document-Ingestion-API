import sqlalchemy
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
)
from datetime import datetime

# --- Database Setup ---
DATABASE_URL = "sqlite:///./ingestion_metadata.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

# --- Table Definition ---
documents_table = Table(
    "documents",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("filename", String, nullable=False),
    Column("file_hash", String, nullable=False, unique=True),
    Column("chunking_strategy", String, nullable=False),
    Column("status", String, default="processing"),
    Column("chunk_count", Integer, nullable=True),
    Column("ingested_at", DateTime, default=datetime.utcnow),
)

# --- Service Class ---
class MetadataDBService:
    def create_db_and_tables(self):
        """Initializes the database and creates tables if they don't exist."""
        metadata.create_all(engine)

    def add_document(self, filename: str, file_hash: str, strategy: str) -> int:
        """Adds a new document record to the database and returns its ID."""
        query = documents_table.insert().values(
            filename=filename,
            file_hash=file_hash,
            chunking_strategy=strategy,
            status="processing",
        )
        with engine.connect() as conn:
            result = conn.execute(query)
            conn.commit()
            return result.inserted_primary_key[0]

    def update_document_status(self, doc_id: int, status: str, chunk_count: int = None):
        """Updates the status and chunk count of a document."""
        query = (
            documents_table.update()
            .where(documents_table.c.id == doc_id)
            .values(status=status, chunk_count=chunk_count)
        )
        with engine.connect() as conn:
            conn.execute(query)
            conn.commit()

    def find_document_by_hash(self, file_hash: str):
        """Finds a document by its content hash to check for duplicates."""
        query = documents_table.select().where(documents_table.c.file_hash == file_hash)
        with engine.connect() as conn:
            result = conn.execute(query)
            return result.fetchone()


# Create a single, reusable instance of the service
metadata_db_service = MetadataDBService()