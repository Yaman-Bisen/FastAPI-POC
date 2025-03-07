from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        form_attributes = True

class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[UserResponse] = None


class UserDelete(BaseModel):
    id: int = Field(..., gt=0, description="User ID to delete")