"""Configuration settings for the Chess Analysis Server."""
import os
from pathlib import Path
from dotenv import load_dotenv
import tomllib


def _get_version_from_pyproject() -> str:
    """Read version from pyproject.toml file."""
    pyproject_paths = [
        Path(__file__).parent.parent / "pyproject.toml",
        Path.cwd() / "pyproject.toml",  
        Path.cwd() / "backend" / "pyproject.toml",  
    ]
    
    for pyproject_path in pyproject_paths:
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("project", {}).get("version", "0.1.0")
            except Exception:
                pass
    
    return "0.1.0"


# Try multiple possible locations for .env file
env_paths = [
    Path(__file__).parent.parent / ".env",  # backend/.env
    Path.cwd() / ".env",  # Current working directory
    Path.cwd() / "backend" / ".env", 
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path, override=True)
        break


class Config:

    
    def __init__(self):
        # Flask settings
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development" if self.DEBUG else "production")
        self.APP_VERSION = _get_version_from_pyproject()
        
        # Database settings
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        
        # Neo4j settings
        self.NEO4J_HOST = os.getenv("NEO4J_HOST")
        self.NEO4J_PORT = os.getenv("NEO4J_PORT")
        self.NEO4J_USER = os.getenv("NEO4J_USER")
        self.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
        self.NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
        
        # RabbitMQ settings
        self.RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
        self.RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
        self.RABBITMQ_USER = os.getenv("RABBITMQ_USER")
        self.RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
        self.RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST")
    
    @property
    def DATABASE_URI(self) -> str:
        """Get PostgreSQL database URI."""
        if not all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_NAME]):
            missing = [k for k, v in {
                "DB_USER": self.DB_USER,
                "DB_PASSWORD": self.DB_PASSWORD,
                "DB_HOST": self.DB_HOST,
                "DB_PORT": self.DB_PORT,
                "DB_NAME": self.DB_NAME
            }.items() if v is None]
            raise ValueError(f"Missing required database configuration: {', '.join(missing)}")
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def NEO4J_URI(self) -> str:
        """Get Neo4j database URI."""
        if not all([self.NEO4J_HOST, self.NEO4J_PORT]):
            missing = [k for k, v in {
                "NEO4J_HOST": self.NEO4J_HOST,
                "NEO4J_PORT": self.NEO4J_PORT
            }.items() if v is None]
            raise ValueError(f"Missing required Neo4j configuration: {', '.join(missing)}")
        return f"bolt://{self.NEO4J_HOST}:{self.NEO4J_PORT}"
    
    @property
    def RABBITMQ_BROKER_URL(self) -> str:
        """Get RabbitMQ broker URL."""
        if not all([self.RABBITMQ_USER, self.RABBITMQ_PASSWORD, self.RABBITMQ_HOST, self.RABBITMQ_PORT]):
            missing = [k for k, v in {
                "RABBITMQ_USER": self.RABBITMQ_USER,
                "RABBITMQ_PASSWORD": self.RABBITMQ_PASSWORD,
                "RABBITMQ_HOST": self.RABBITMQ_HOST,
                "RABBITMQ_PORT": self.RABBITMQ_PORT
            }.items() if v is None]
            raise ValueError(f"Missing required RabbitMQ configuration: {', '.join(missing)}")
        vhost = (self.RABBITMQ_VHOST or "/").lstrip("/")
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{vhost}"


config = Config()
