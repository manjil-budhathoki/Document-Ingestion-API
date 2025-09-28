import redis
import json
from typing import List, Dict

class RedisMemoryService:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """Initializes the Redis client."""
        # The decode_responses=True is important to get strings back from Redis
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retrieves the chat history for a given session ID.
        History is stored as a list of JSON strings in Redis.
        """
        try:
            # lrange returns a list of items from the list in Redis
            history_json = self.client.lrange(session_id, 0, -1)
            # Each item is a JSON string, so we need to parse it
            return [json.loads(item) for item in history_json]
        except redis.RedisError as e:
            print(f"Redis error getting chat history: {e}")
            return []

    def add_to_chat_history(self, session_id: str, user_message: str, ai_message: str):
        """
        Adds a new user message and its corresponding AI response to the history.
        """
        try:
            # Add the user's message
            self.client.rpush(session_id, json.dumps({"role": "user", "content": user_message}))
            # Add the AI's response
            self.client.rpush(session_id, json.dumps({"role": "assistant", "content": ai_message}))
        except redis.RedisError as e:
            print(f"Redis error adding to chat history: {e}")

# Create a single, reusable instance of the service
memory_service = RedisMemoryService()