from __future__ import annotations  # allows forward references without quotes

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pgsql


class User(SQLModel, table=True):
    # allow SQLAlchemy Mapped[...] / other arbitrary types to be accepted by pydantic-core
    model_config = {"arbitrary_types_allowed": True, "from_attributes": True}
    # allow redefinition of the table (useful with auto-reload / multiple imports)
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str

    # Relationships (excluded from Pydantic schema)
    transactions: list["Transaction"] = Relationship(back_populates="user")
    received_transactions: list["Transaction"] = Relationship(back_populates="recipient_user")


class Transaction(SQLModel, table=True):
    # allow SQLAlchemy Mapped[...] / other arbitrary types to be accepted by pydantic-core
    model_config = {"arbitrary_types_allowed": True, "from_attributes": True}
    # allow redefinition of the table (useful with auto-reload / multiple imports)
    __table_args__ = {"extend_existing": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)

    # 'CREDIT', 'DEBIT', 'TRANSFER_IN', 'TRANSFER_OUT'
    transaction_type: str = Field(nullable=False)
    amount: float = Field(nullable=False, default=0)
    description: Optional[str] = Field(default=None, sa_column=Column(pgsql.TEXT))

    # self-referential FK
    reference_transaction_id: Optional[UUID] = Field(default=None, foreign_key="transaction.id")

    # recipient user for transfer transactions
    recipient_user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships (excluded from Pydantic schema)
    user: "User" = Relationship(back_populates="transactions")
    recipient_user: "User" = Relationship(back_populates="received_transactions")
    reference_transaction: "Transaction" = Relationship(
        back_populates="child_transactions",
        sa_relationship_kwargs={"remote_side": "Transaction.id"}
    )
    child_transactions: list["Transaction"] = Relationship(back_populates="reference_transaction")
