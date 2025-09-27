from fastapi import FastAPI
from api import ingestion

app = FastAPI(
    title="Document Ingestion API",
    description="API for uploading documents and extracting text from them.",
    version="1.0.0",
)


# Include the router from the api.ingestion module
# This makes all the routes defined in that router available in our app
app.include_router(ingestion.router)

@app.get("/", tags=["Root"])
def read_root() -> dict:
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Document Ingestion API!"}