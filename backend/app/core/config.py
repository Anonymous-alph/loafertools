import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"

class Settings(BaseSettings):
    MODE: ModeEnum = ModeEnum.development
    DATABASE_URL: str
    SECRET_KEY: str = "your-secret-key"
    
    model_config = SettingsConfigDict(
        case_sensitive=True, 
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()

