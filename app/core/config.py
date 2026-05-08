from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Career Inbox Intelligence"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery (Defaults to REDIS_URL if not provided)
    CELERY_BROKER_URL: str | None = None
    CELERY_RESULT_BACKEND: str | None = None
    
    # OpenAI
    OPENAI_API_KEY: str = "your_openai_api_key"
    
    # Groq
    GROQ_API_KEY: str = "your_groq_api_key"
    
    # Google OAuth2
    GOOGLE_CLIENT_ID: str = "your_client_id"
    GOOGLE_CLIENT_SECRET: str = "your_client_secret"
    GOOGLE_REFRESH_TOKEN: str = "your_refresh_token"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = "your_bot_token"
    TELEGRAM_CHAT_ID: str = "your_chat_id"
    
    # LangSmith (Observability)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str = "ai-interview-notifier"
    
    @property
    def broker_url(self) -> str:
        return self.CELERY_BROKER_URL or self.REDIS_URL
        
    @property
    def result_backend(self) -> str:
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def export_to_env(self):
        """Export LangSmith settings to environment variables for LangChain's automatic tracing."""
        import os
        if self.LANGCHAIN_TRACING_V2:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_ENDPOINT"] = self.LANGCHAIN_ENDPOINT
            if self.LANGCHAIN_API_KEY:
                os.environ["LANGCHAIN_API_KEY"] = self.LANGCHAIN_API_KEY
            os.environ["LANGCHAIN_PROJECT"] = self.LANGCHAIN_PROJECT

settings = Settings()
settings.export_to_env()
