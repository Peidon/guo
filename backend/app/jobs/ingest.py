from datetime import datetime, timezone

from services.metal_service import fetch_metal_price
from services.stock_service import fetch_stock_price
from core.db import SessionLocal
from models.metal_price import MetalPrice
from models.stock_price import StockPrice
from loguru import logger

Currency = ["AUD", "USD"]
MetalSymbol = ["XAU", "XAG", "XPT", "XPD"] # Gold, Silver, Platinum, Palladium

def adapt(data):
    data['timestamp'] = datetime.fromtimestamp(data['timestamp'], tz=timezone.utc)
    data['open_time'] = datetime.fromtimestamp(data['open_time'], tz=timezone.utc)
    return data

def ingest_gold():
    db = SessionLocal()
    data = fetch_metal_price("XAU", "USD")
    if not data:
        logger.error("Failed to fetch gold price. ")
        return
    data = adapt(data)
    record = MetalPrice(**data)
    db.add(record)
    db.commit()
    db.close()

from core.enumerate import StockSymbols

def ingest_stocks():
    db = SessionLocal()

    syms = []
    for symbol in StockSymbols:
        data = fetch_stock_price(symbol)
        if not data:
            syms.append(symbol)
            continue

        record = StockPrice(**data)
        db.add(record)

    if len(syms) > 0:
        logger.error("Failed to fetch stock prices {0}".format(syms))

    db.commit()
    db.close()