from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class WalletBalanceResponseModel(BaseModel):
    user_id: UUID
    balance: float
    last_updated: datetime

class WalletAddMoneyRequestModel(BaseModel):
    amount:float
    description:str

class WalletAddMoneyResponseModel(BaseModel):
    transaction_id: UUID
    user_id: UUID
    amount: float
    new_balance: float
    transaction_type: str

class WalletWithdrawMoneyRequestModel(BaseModel):
    amount:float
    description:str
