from sqlmodel import SQLModel
from app.models.user_model import Transaction
from typing import List
from pydantic import BaseModel

class TransactionPaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    transactions: List[Transaction]
    class Config:
        orm_mode = True

class TransactionResponse(Transaction):
    pass


