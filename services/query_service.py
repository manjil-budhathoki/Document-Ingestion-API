from services.embedding_service import embedding_service
from services.vector_db_service import vector_db_service, QDRANT_COLLECTION_NAME
from services.llm_service import llm_service
from services.memory_service import memory_service
from typing import List, Dict, Any

def _create_standalone_question(chat_history: List[Dict[str, str]], user_query: str) -> str:
    """
    Uses the LLM to rephrase the user's query into a standalone question
    based on the chat history.
    """
    # If there's no history, the original query is already standalone
    if not chat_history:
        return user_query

    # Format the chat history into a string
    history_str = "\n".join([f"{item['role']}: {item['content']}" for item in chat_history])
    
    # Create a prompt for the LLM to rephrase the question
    rephrase_prompt = f"""
    Given the following conversation history and a follow-up question,
    rephrase the follow-up question to be a standalone question.

    Chat History:
    {history_str}

    Follow-up Question: {user_query}

    Standalone Question:
    """
    
    # Use the LLM to generate the standalone question
    # This is a second, much faster call to the LLM
    standalone_question = llm_service.generate_response(rephrase_prompt)
    return standalone_question.strip()



def _build_prompt(question: str, context: List[Dict[str, Any]]) -> str:
    """Builds a detailed prompt for the Gemini model."""
    
    # Consolidate the context from the search results into one string
    context_str = "\n\n---\n\n".join([item['chunk_text'] for item in context])
    
    prompt = f"""
    Based ONLY on the context provided below, answer the user's question.
    Do not use any external knowledge.
    If the context does not contain the answer, you MUST say "The provided context does not contain enough information to answer this question."

    CONTEXT:
    {context_str}

    QUESTION:
    {question}
    """
    return prompt

def process_query(user_query: str, session_id: str) -> str:
    """
    Processes a user's query using the RAG pipeline with query rephrasing.
    """
    # 1. Load chat history
    chat_history = memory_service.get_chat_history(session_id)
    
    # 2. Create a standalone question based on the history
    standalone_question = _create_standalone_question(chat_history, user_query)
    print(f"Original question: '{user_query}'")
    print(f"Standalone question: '{standalone_question}'")

    # 3. Generate embedding for the STANDALONE question
    query_embedding = embedding_service.generate_embeddings([standalone_question])[0]
    
    # 4. Search Qdrant using the new embedding
    search_results = vector_db_service.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding
    )
    
    # 5. Build the final prompt for the answer
    prompt = _build_prompt(standalone_question, search_results)
    
    # 6. Generate the final answer (This is the slow part)
    final_answer = llm_service.generate_response(prompt)
    
    # 7. Save the ORIGINAL question and the final answer to history
    memory_service.add_to_chat_history(session_id, user_query, final_answer)

    return final_answer


