from fastapi import Depends, Request, HTTPException
from app.models import Users
from config.Database.database import db_manager
from app.schemas.users import UserCreate, UserResponse, ResponseModel, UserDelete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete
# from fastapi_utils.cbv import cbv

async def index():
    return JSONResponse(content={"error": "Hello FastAPI"}, status_code=200)



class UserAPI:
    def __init__(self):
        pass

    async def create_user(self, user: UserCreate, db: AsyncSession = Depends(db_manager.get_db)):
        try:
            stmt = select(Users).where(Users.email == user.email)
            result = await db.execute(stmt)
            existing_user = result.scalars().first()

            if existing_user:
                return ResponseModel(
                    status="failure",
                    message="User with this email already exists."
                )


            new_user = Users(name=user.name, email=user.email)
            db.add(new_user)

            await db.commit() 
            await db.refresh(new_user) 

            user_response = UserResponse(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email
            )
                        
            return ResponseModel(
                status="success",
                message="User created successfully.",
                data=user_response
            )
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database error occurred"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred, {e}"
            )
        
    async def delete_user(self, user_id: UserDelete, db: AsyncSession = Depends(db_manager.get_db)):
        try:
            stmt = select(Users).where(Users.id == user_id.id)
            result = await db.execute(stmt)
            existing_user = result.scalars().first()
            
            if not existing_user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            
            delete_stmt = delete(Users).where(Users.id == user_id.id)
            await db.execute(delete_stmt)
            await db.commit()
            
            return ResponseModel(
                status="success",
                message=f"User with ID {user_id} deleted successfully"
            )
            
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error occurred, {e}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred, {e}"
            )