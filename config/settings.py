from .base import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME = "FastAPI Django-Style Project"
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    ENV = "dev"

    MIDDLEWARES = [
        "app.middlewares.allowed_hosts.check_allowed_hosts"
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
        "secondary": {
            "ENGINE": "postgresql+asyncpg",
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": "fa_test_2",
            "USER": "postgres",
            "PASSWORD": "postgres",
        }
    }

settings = Settings()