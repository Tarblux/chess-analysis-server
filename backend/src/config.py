"""Configuration settings for the Chess Analysis Server."""
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / ".env"

# Load .env file (override=True ensures it actually loads the values....right? lol)
if env_path.exists():
    load_dotenv(env_path, override=True)
else:
    # Try loading from current working directory as fallback
    load_dotenv(Path.cwd() / ".env", override=True)


class Config:

    
    def __init__(self):
        # Flask settings
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        
        # Database settings
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_NAME = os.getenv("DB_NAME", "chess_analysis")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    
    @property
    def DATABASE_URI(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()
