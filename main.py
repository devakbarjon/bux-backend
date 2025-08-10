from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.logging_config import logger
from app.api.v1.router import router as api_v1_router
from app.services.bot.bot_base import bot


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database models initialized.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # Initialize database models
    yield
    await bot.session.close()
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url} {request.client.host}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response