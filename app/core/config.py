from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Document Search & RAG Platform"
    database_url: str
    redis_url: str

    # Quotas (guide ke hisaab se, config se badal sakte hain)
    max_file_size_mb: int = 10
    max_storage_per_user_mb: int = 100
    max_documents_per_user: int = 20
    max_questions_per_month: int = 50
    max_question_length: int = 2000
    retrieval_top_k: int = 5

    cors_origins: list[str] = ["http://localhost:5173"] 

settings = Settings()