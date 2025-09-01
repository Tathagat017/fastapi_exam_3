from sqlite3 import IntegrityError

from sqlmodel.ext.asyncio.session import AsyncSession
from app.schema.user_schema import UserCreateRequestModel,UserResponseModel,UserUpdateRequestModel
from app.models.user_model import User
from sqlmodel import select

class UserService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, new_user: UserCreateRequestModel):
        new_user = User(**new_user.model_dump())
        self.session.add(new_user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        response = UserResponseModel(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            phone_number=new_user.phone_number,
            balance=new_user.balance,
            created_at=new_user.created_at,
        )
        return response


    async def get_user(self, user_id: str):
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        user = result.first()
        response = UserResponseModel(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            balance=user.balance,
            created_at=user.created_at,
        )
        return response


    async def delete_user(self, user_id: str):
        pass

    async def update_user(self, user_id: str, user: UserUpdateRequestModel):
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.first()
        if user:
            for key, value in user.model_dump().items():
                setattr(user, key, value)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        response = UserResponseModel(
            id=user.id,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            balance=user.balance,
            created_at=user.created_at,
        )
        return response

