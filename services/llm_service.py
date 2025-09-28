import google.generativeai as genai
from config import settings

class LLMService:
    def __init__(self):
        """Initializes the Gemini client with the API key."""
        genai.configure(api_key=settings.gemini_api_key)
        # We'll use 'gemini-2.5-flash' as it's the standard model for text generation
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_response(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini model and returns the text response.
        """
        try:
            response = self.model.generate_content(prompt)
            # Return the text from the response
            return response.text
        except Exception as e:
            # Basic error handling in case the API call fails
            print(f"Error calling Gemini API: {e}")
            return "I'm sorry, I encountered an error while trying to generate a response."

# Create a single instance to be used throughout the app
llm_service = LLMService()