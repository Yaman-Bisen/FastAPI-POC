import os
from pathlib import Path
from .base import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME = "FastAPI Django-Style Project"
    ENV = "dev"

    HOST_NAME = os.uname()[1]
    BASE_DIR = Path(__file__).resolve().parent.parent

    ALLOWED_HOSTS = [
        "http://localhost:8000"
    ]

    ALLOWED_METHODS = ['*']
    ALLOWED_HEADERS = ['*']
    ALLOWED_CREDENTIALS = True



    MIDDLEWARES = [
        "starlette_csrf.CSRFMiddleware"
    ]

    DATABASES = {
        "default": {
            "ENGINE": "postgresql+asyncpg",
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": "fa_test_1",
            "USER": "postgres",
            "PASSWORD": "postgres",
        },
        # "secondary": {
        #     "ENGINE": "postgresql+asyncpg",
        #     "HOST": "localhost",
        #     "PORT": 5432,
        #     "NAME": "fa_test_2",
        #     "USER": "postgres",
        #     "PASSWORD": "postgres",
        # }
    }

settings = Settings()