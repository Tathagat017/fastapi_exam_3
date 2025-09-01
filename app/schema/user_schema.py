from datetime import datetime

from pydantic import BaseModel
from app.models.user_model import User
from typing import Optional
from uuid import UUID



class UserCreateRequestModel(BaseModel):
    username: str
    password: str
    email: str
    phone_number: Optional[str]
    class Config:
        orm_mode = True

class UserResponseModel(BaseModel):
    id:UUID
    username: str
    email: str
    phone_number: str
    balance:float
    created_at:datetime
    class Config:
        orm_mode = True

class UserUpdateRequestModel(BaseModel):
    username: str
    password: str
    email: str