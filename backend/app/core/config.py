from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    app_name: str = "Personal CFO"
    secret_key: str = Field(..., alias="SECRET_KEY")
    environment: str = "development"
    
    database_url: str = Field(..., alias="DATABASE_URL")
    
    plaid_client_id: str = Field(..., alias="PLAID_CLIENT_ID")
    plaid_secret: str = Field(..., alias="PLAID_SECRET")
    plaid_env: str = Field("sandbox", alias="PLAID_ENV")
    
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    cookie_secure: bool = Field(True, alias="COOKIE_SECURE")
    cookie_samesite: str = Field("Strict", alias="COOKIE_SAMESITE")
    
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"], alias="CORS_ORIGINS")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
