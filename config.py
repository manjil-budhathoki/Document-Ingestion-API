from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Loads application settings from the .env file."""
    gemini_api_key: str

    # This tells Pydantic to look for a file named .env
    model_config = SettingsConfigDict(env_file=".env")

# Create a single, reusable instance of the settings
settings = Settings()