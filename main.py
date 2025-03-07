from fastapi import FastAPI
from app.urls import app_router
from app.management import setup_commands
from app.middlewares.setup import setup_middlewares
from config.Database.database import db_manager


async def lifespan(app: FastAPI):
    await db_manager.validate_connections()
    commands = setup_commands.setup_commands()
    # Yield control back to the application
    yield

    # Cleanup actions (if needed) when shutting down

app = FastAPI(title="FastAPI Django-Style Project", lifespan=lifespan)
# Register app-specific routers
app.include_router(app_router, prefix="/app")
setup_middlewares(app)