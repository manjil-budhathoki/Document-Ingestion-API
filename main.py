from fastapi import FastAPI
from api import ingestion
from services.database_service import metadata_db_service # Import the service

# Add a startup event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    print("Initializing database...")
    metadata_db_service.create_db_and_tables()
    print("Database initialized.")
    yield
    # Code below yield runs on shutdown (if any needed)

app = FastAPI(
    title="Document Ingestion API",
    description="An API to upload documents, extract text, and prepare for embedding.",
    version="1.0.0",
    lifespan=lifespan # Attach the lifespan manager
)

app.include_router(ingestion.router)

@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "Welcome to the Document Ingestion API!"}