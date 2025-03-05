from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi.responses import JSONResponse
from app.models import UserDB1
from config.Database.database import db_manager
# async def get_db():
#     async with SessionLocal() as db:
#         yield db

async def index():
    return JSONResponse(content={"error": "Hello FastAPI"}, status_code=200)

async def create_user(request: Request):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {"error": "Name and email are required"}

    user = UserDB1(
        name=name,
        email=email
    )
    new_user = await db_manager.create(user)

    if not new_user:
        return {"message": "User not created"}

    return {"message": "User created successfully", "id": new_user.id}

async def delete_user(request: Request):
    data = await request.json()
    user_id = data.get("user_id")

    user = await db_manager.filter(
        UserDB1,
        {'id': 4}
    )
    
    print(user)

    # user_instance = await db_manager.scaler(query)
    # await db_manager.delete(user_instance, db_name="default", soft_delete=True)

    return {"message": user.id}