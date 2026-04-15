import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Explicitly load .env file to ensure os.environ is populated
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "TicTacToe API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # These will be loaded from .env automatically by pydantic-settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    
    # Use Union to allow the environment string "url1,url2" to not fail initial parsing
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return v
    
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
