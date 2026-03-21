from datetime import datetime, timezone

import requests
from core.db import SessionLocal
from core.config import settings
from loguru import logger
from models.metal_price import MetalPrice
from sqlalchemy import select


def get_history_price(symbol, begin, end) -> list:
    """
    :param symbol: Metal Symbol "XAU", "XAG", "XPT", "XPD"
    :param begin: timestamp
    :param end: timestamp
    :return: list[ chart_data{time: number, price: number} ]
    """
    begin_time = datetime.fromtimestamp(begin, tz=timezone.utc)
    end_time = datetime.fromtimestamp(end, tz=timezone.utc)

    db = SessionLocal()
    try:
        rows = db.execute(
            select(MetalPrice.timestamp, MetalPrice.price)
            .where(
                MetalPrice.metal == symbol,
                MetalPrice.timestamp >= begin_time,
                MetalPrice.timestamp <= end_time,
                MetalPrice.price.is_not(None),
            )
            .order_by(MetalPrice.timestamp.asc())
        ).all()
    finally:
        db.close()

    return [{"time": int(timestamp.timestamp()), "price": float(price)} for timestamp, price in rows]

def fetch_metal_price(symbol, curr, date = ""):
    """
    :param symbol: Metal Symbol "XAU", "XAG", "XPT", "XPD"
    :param curr: Currency Code "AUD", "USD" etc.
    :param date: "/20260318"
    :return:
    """

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": settings.METAL_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error("gold api error {x}", x=e)