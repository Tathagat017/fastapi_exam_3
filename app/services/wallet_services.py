from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schema.wallet_schema import WalletAddMoneyResponseModel, WalletAddMoneyRequestModel,WalletWithdrawMoneyRequestModel,WalletBalanceResponseModel
from app.models.user_model import User
from app.models.transaction_model import Transaction


class WalletService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_wallet_balance(self, user_id: str):
        statement = select(User).where(User.id == user_id)
        result = await self.session.exec(statement)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        balance = WalletBalanceResponseModel(
            user_id=user.id,
            balance=user.balance,
            last_updated = user.last_balance_update
        )
        return balance

    async def add_money(self, user_id: str,request: WalletAddMoneyRequestModel):
        statement = select(User).where(User.id == user_id)
        result = await self.session.exec(statement)
        user = result.first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        new_transaction = Transaction(amount=request.amount, description=request.description, user_id=user_id,
                                      transaction_type="CREDIT", recipient_user_id=user_id)
        try:
            self.session.add(new_transaction)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Internal server error")
        await self.session.refresh(new_transaction)
        user.balance += request.amount
        user.last_balance_update = datetime.now()
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=409, detail="Error adding money")
        await self.session.refresh(user)
        response = WalletAddMoneyResponseModel(
            user_id=user.id,
            transaction_id = new_transaction.id,
            amount = new_transaction.amount,
            new_balance=user.balance,
            transaction_type=new_transaction.transaction_type,
        )
        return response



    async def withdraw(self, user_id: str,request: WalletWithdrawMoneyRequestModel):
        statement = select(User).where(User.id == user_id)
        result = await self.session.exec(statement)
        user = result.first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.balance < request.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        user.balance -= request.amount
        user.last_balance_update = datetime.now()
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=409, detail="Internal server error")
        await self.session.refresh(user)
        return user.balance
