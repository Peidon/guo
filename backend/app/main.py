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


from services.signal import classify, compute_score, load_data, normalize, score_max, score_min
from services.metal_service import get_history_price

@api.get("/")
def hello():
    return "Hello, I'm jing service. "

@api.get("/gold")
def get_gold(begin: int, end: int, symbol: str = "XAU"):
    prices = get_history_price(symbol, begin, end)
    return prices

@api.get("/signals/{symbol}")
def get_signal(symbol: str):
    data = load_data(symbol)
    raw_score = compute_score(data)
    normalized_score = normalize(raw_score, score_min, score_max)

    return {
        "symbol": symbol,
        "raw_score": raw_score,
        "score": normalized_score,
        "factors": {
            "gold_beta": data.get('gold_beta'),
            "relative_strength": data.get('relative_strength'),
            "momentum": data.get('momentum'),
            "volatility": data.get('volatility'),
            "liquidity": data.get('liquidity')
        },
        "action": classify(normalized_score)
    }

from core.enumerate import StockSymbols

@api.get("/stocks")
def get_stocks():
    return StockSymbols