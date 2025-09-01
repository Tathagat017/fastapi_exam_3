from datetime import datetime
from typing import Optional,List

from sqlalchemy.orm import relationship
from sqlmodel import Field, Column,SQLModel
import sqlalchemy.dialects.postgresql as pgsql
from uuid import UUID,uuid4


class User(SQLModel, table=True):
    id:UUID = Field(default_factory=uuid4, primary_key=True,unique=True)
    username:str = Field(nullable=False)
    password:str = Field(nullable=False)
    email:str = Field(nullable=False)
    phone_number:Optional[str] = Field(nullable=True)
    balance:float = Field(nullable=False,default=0)
    last_balance_update:datetime = Field(nullable=False,default=datetime.now())
    created_at:datetime = Field(sa_column=Column(pgsql.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pgsql.TIMESTAMP, default=datetime.now))
    transactions:List["Transaction"] = relationship(back_populates="user")

class Transaction(SQLModel, table=True):
    id:UUID = Field(default_factory=uuid4, primary_key=True,unique=True)
    user_id:UUID = Field(foreign_key="user.id")
    #'CREDIT', 'DEBIT', 'TRANSFER_IN', 'TRANSFER_OUT'
    transaction_type:str = Field(nullable=False)
    amount:float = Field(nullable=False,default=0)
    description:str = Field(sa_column=Column(pgsql.TEXT))
    reference_transaction_id:UUID = Field(foreign_key="transaction.reference_transaction_id")
    #recipient user id for transfer transactions
    recipient_user_id:UUID = Field(foreign_key="user.id")
    created_at:datetime = Field(sa_column=Column(pgsql.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pgsql.TIMESTAMP, default=datetime.now))
    transactions:"User" = relationship(back_populates="transactions")