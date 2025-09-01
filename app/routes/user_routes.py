from fastapi import APIRouter, Depends

from app.models.user_model import User
from app.schema.user_schema import UserResponseModel, UserCreateRequestModel,UserUpdateRequestModel
from http import HTTPStatus
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import get_session
from app.services.user_services import UserService
user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.get("/{user_id}",response_model=UserResponseModel,status_code=HTTPStatus.OK)
async def get_user(user_id: int,session:AsyncSession = Depends(get_session)):
    return await UserService(session).get_user(user_id)

@user_router.post("/",response_model=UserResponseModel,status_code=HTTPStatus.CREATED)
async def create_user(user: UserCreateRequestModel,session:AsyncSession = Depends(get_session)):
    return await UserService(session).create_user(user)

@user_router.put("/{user_id}",response_model=UserResponseModel,status_code=HTTPStatus.OK)
async def update_user(user_id:str,user: UserUpdateRequestModel,session:AsyncSession = Depends(get_session)):
    return await UserService(session).update_user(user_id,user)

@user_router.delete("/{user_id}",status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int,session:AsyncSession = Depends(get_session)):
    pass