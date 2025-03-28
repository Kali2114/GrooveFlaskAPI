"""Configuration for app."""

import os
from dotenv import load_dotenv
from pathlib import Path


base_dir = Path(__file__).resolve().parent
env_file = base_dir / ".env"
load_dotenv()


class Config:
    DEBUG = os.getenv("FLASK_DEBUG")
    ENV = os.getenv("FLASK_ENV")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 5
    JWT_EXPIRED_MINUTES = 60


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class TestingConfig(Config):
    DB_FILE_PATH = base_dir / "tests" / "test.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_FILE_PATH}"
    DEBUG = True
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
