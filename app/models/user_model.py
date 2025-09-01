from datetime import datetime

from typing import Optional
from sqlmodel import Field, Column,SQLModel,Relationship
import sqlalchemy.dialects.postgresql as pgsql
from uuid import UUID,uuid4



class User(SQLModel, table=True):
    id:UUID = Field(sa_column=Column(pgsql.UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, index=True))
    username:str = Field(nullable=False)
    password:str = Field(nullable=False)
    email:str = Field(nullable=False)
    phone_number:Optional[str] = Field(nullable=True)
    balance:float = Field(nullable=False,default=0)
    last_balance_update:datetime = Field(nullable=False,default=datetime.now())
    created_at:datetime = Field(sa_column=Column(pgsql.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pgsql.TIMESTAMP, default=datetime.now))
    # transactions:list["Transaction"] = Relationship(back_populates="user")
    
    class Config:
        arbitrary_types_allowed = True
 

class Transaction(SQLModel, table=True):
    id:UUID = Field(sa_column=Column(pgsql.UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, index=True))
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
    # user:list[User] = Relationship(back_populates="transactions")
    class Config:
        arbitrary_types_allowed = True
