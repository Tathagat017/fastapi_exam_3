from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class TransactionResponse(BaseModel):
    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}

    id: UUID
    user_id: UUID
    transaction_type: str
    amount: float
    description: Optional[str] = None
    reference_transaction_id: Optional[UUID] = None
    recipient_user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

class TransactionPaginatedResponse(BaseModel):
    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}

    total: int
    page: int
    size: int
    transactions: List[TransactionResponse]


