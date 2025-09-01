import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.transaction_routes import transaction_router
from app.db.database import init_db
from app.routes.user_routes import user_router
from app.routes.wallet_routes import wallet_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan start")
    await init_db()
    yield
    print("lifespan end")

app = FastAPI(
    title="Payment Service Backend",
    description="Payment Service Backend",
    version="1.0",
    lifespan=lifespan,
)

app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(transaction_router)

@app.get("/health")
async def health():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("app.server:app", host="0.0.0.0", port=8010,reload=True)