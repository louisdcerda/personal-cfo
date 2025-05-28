from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Personal CFO"
    plaid_client_id: str
    plaid_secret: str
    plaid_env: str = "sandbox"

    class Config:
        env_file = ".env"

settings = Settings()

