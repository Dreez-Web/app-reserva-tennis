import os
from pathlib import Path
from dotenv import load_dotenv

# cargar .env si existe
env_path = Path(__file__).absolute().parents[1] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:martin108@localhost:5433/tennisdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
