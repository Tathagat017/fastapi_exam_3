
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.schema.transaction_schema import TransactionPaginatedResponse
from app.models.transaction_model import Transaction


class TransactionService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_paginated_transactions(self,  limit: int = 100,page:int = 1):
        stmt = select(Transaction).order_by(Transaction.created_at)
        result = await self.session.execute(stmt)
        total  = len(result.all())
        #return all the paginated transactions
        trns = result.all()[(page-1)*limit:page*limit]
        response = TransactionPaginatedResponse(
            total=total,
            page=page,
            limit=limit,
            transactions=trns
        )
        return response
        

    async def get_transaction_by_id(self, transaction_id: str):
        stmt = select(Transaction).where(Transaction.id == transaction_id)
        result = await self.session.execute(stmt)
        trn = result.scalar_one_or_none()
        if not trn:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return trn
