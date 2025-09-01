from fastapi import APIRouter,Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import get_session
from app.services.transaction_services import TransactionService
from app.schema.transaction_schema import TransactionPaginatedResponse,TransactionResponse

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["transaction"]
)

@transaction_router.get("/{user_id}?page={page}&limit={limit}", response_model=TransactionPaginatedResponse, status_code=200)
async def get_paginated_transactions(user_id: str,page:int = 0, limit:int = 10,session:AsyncSession= Depends(get_session)):
    return await TransactionService(session).get_all_paginated_transactions(limit=limit,page=page)
    

@transaction_router.get("/detail/{transaction_id}", response_model=TransactionResponse, status_code=200)
async def get_transaction_by_id(transaction_id:str,session:AsyncSession= Depends(get_session)):
    return await TransactionService(session).get_transaction_by_id(transaction_id)

