from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, chat, gamification, market
from app.services.smartkarma_mcp import mcp_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await mcp_client.close()


app = FastAPI(
    title="Finny API",
    description="Financial Literacy App for Kids — Powered by Smartkarma",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(market.router)
app.include_router(gamification.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "finny"}
