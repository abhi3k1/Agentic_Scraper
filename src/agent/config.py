try:
    # pydantic v2+ moved BaseSettings to pydantic-settings
    from pydantic_settings import BaseSettings
except Exception:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str | None = None
    google_application_credentials: str | None = None
    google_project: str | None = None
    google_location: str = "us-central1"
    llm_provider: str = "google_genai"
    model_name: str = "gemini-2.5-flash-lite"
    database_url: str = "sqlite:///./agent_data.db"
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
