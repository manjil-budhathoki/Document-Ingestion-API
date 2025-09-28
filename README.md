# Document Ingestion and RAG API

A backend-only project that implements a full Retrieval-Augmented Generation (RAG) pipeline. The system allows users to upload documents and then have a conversation about their content.

This project was built using **FastAPI**, **Qdrant**, **Redis**, and **Google Gemini Pro**.

---

## Features

-   **Document Ingestion**: Upload `.pdf` or `.txt` files, which are then chunked, vectorized, and stored.
-   **Conversational RAG**: Ask questions about the uploaded documents.
-   **Chat Memory**: Remembers conversation history to understand follow-up questions.
-   **Interview Booking**: Detects user intent to schedule an interview and saves the details.

---

## Setup and Installation

### Prerequisites
-   **Python 3.10+**
-   **Conda** or another virtual environment manager
-   **Docker**

### Step 1: Clone the Repository

```bash
git clone https://github.com/manjil-budhathoki/Document-Ingestion-API.git
cd Document-Ingestion-API
```

### Step 2: Set Up the Python Environment

Create and activate a Conda environment, then install the required packages.

```bash
# Create and activate the Conda environment
conda create --name document_api python=3.10 -y
conda activate document_api

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a file named `.env` in the root of the project. This file will hold your API key.

```ini
# .env
GEMINI_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"
```

### Step 4: Run a simple command to bring up both your Redis and Qdrant containers

```bash
docker-compose up -d 
```

---

## Running the Application

With the database and cache services running, start the FastAPI server.

```bash
uvicorn main:app --reload
```

The API is now running. You can access the interactive documentation (Swagger UI) at:
**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## How to Use

All interaction with the API can be done through the `/docs` page.

1.  **Ingest a Document**:
    -   Use the `POST /ingest/` endpoint.
    -   Select a `.pdf` or `.txt` file and execute.

2.  **Ask a Question**:
    -   Use the `POST /chat/query/` endpoint.
    -   Provide a `session_id` (e.g., "user-001") and your `question`.
    -   To ask a follow-up question, use the **same** `session_id`.

3.  **Book an Interview**:
    -   Use the `POST /chat/query/` endpoint with a question like "I want to book an interview".
    -   The API will respond with instructions.
    -   Submit the details using the `POST /chat/book-interview/` endpoint.
