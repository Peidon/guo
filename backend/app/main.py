# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from jobs.scheduler import start
import sys
from loguru import logger
# 1. Configure Loguru
logger.remove() # Remove default handler
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | {level} | {message}")
logger.add("logs/app.log", rotation="10 MB", retention="7 days", compression="zip")

@asynccontextmanager
async def lifespan(_: FastAPI):
    start()
    logger.info("jobs started. ")
    yield
    logger.info("Bye~")

api = FastAPI(lifespan=lifespan)


from services.signal import compute_score, load_data, classify

@api.get("/signals/{symbol}")
def get_signal(symbol: str):
    data = load_data(symbol)
    score = compute_score(data)

    return {
        "symbol": symbol,
        "score": score,
        "action": classify(score)
    }