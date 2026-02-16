from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://finny:finny@localhost:5432/finny"
    firebase_credentials_path: str = "firebase-credentials.json"
    smartkarma_mcp_base_url: str = "http://localhost:8080"
    openai_api_key: str = ""
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
