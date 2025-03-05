from fastapi import FastAPI
from app.urls import app_router
from contextlib import asynccontextmanager
from app.middlewares.setup import setup_middlewares
from config.Database.database import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_manager.validate_connections()
    yield

app = FastAPI(title="FastAPI Django-Style Project", lifespan=lifespan)
# Register app-specific routers
app.include_router(app_router, prefix="/app")
setup_middlewares(app)