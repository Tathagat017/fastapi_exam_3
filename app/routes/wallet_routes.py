from fastapi import APIRouter,Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import get_session
from app.schema.wallet_schema import  WalletBalanceResponseModel,WalletAddMoneyResponseModel,WalletAddMoneyRequestModel,WalletWithdrawMoneyRequestModel
from app.services.wallet_services import WalletService
wallet_router = APIRouter(
    prefix="/wallet",
    tags=["wallet"]
)

@wallet_router.get("{user_id}/balance", response_model=WalletBalanceResponseModel, status_code=200)
async def get_wallet_balance(user_id: str,session:AsyncSession= Depends(get_session)):
    return await WalletService(session).get_wallet_balance(user_id)

@wallet_router.post("/{user_id}/add_money", response_model=WalletAddMoneyResponseModel)
async def add_money(user_id:str,request: WalletAddMoneyRequestModel,session:AsyncSession= Depends(get_session)):
    return await WalletService(session).add_money(user_id,request)

@wallet_router.post("/{user_id}/withdraw",response_model=WalletWithdrawMoneyRequestModel)
async def withdraw_money(user_id:str,request: WalletWithdrawMoneyRequestModel,session:AsyncSession= Depends(get_session)):
    return await WalletService(session).withdraw(user_id,request)

