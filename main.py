from fastapi import FastAPI
from api import ingestion, chat
from contextlib import asynccontextmanager
from services.database_service import metadata_db_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    metadata_db_service.create_db_and_tables()
    print("Database initialized.")
    yield
    print("Application Shutdown")

app = FastAPI(
    title="Document Ingestion & RAG API",
    description="An API to upload documents and have a conversation with them.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ingestion.router)
app.include_router(chat.router, prefix="/chat")

@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"message": "Welcome to the Document Ingestion & RAG API!"}