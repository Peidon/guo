from core.db import SessionLocal
from models.metal_price import MetalPrice
from models.stock_price import StockPrice
from sqlalchemy import desc, select

window_width = 20
short_width = 5

def ma_signal(prices):
    """
    volatility
    :param prices: stock prices
    :return: 1 if volatile else -1
    """
    short = sum(prices[-short_width:]) / short_width
    long = sum(prices[-window_width:]) / window_width
    return 1 if short > long else -1

def relative_strength(stock_return, gold_return):
    return stock_return - gold_return

def momentum(prices):
    return (prices[-1] - prices[-(window_width / 2)]) / prices[-(window_width / 2)]

def compute_score(data):
    score = 0

    score += ma_signal(data["prices"]) * 30
    score += momentum(data["prices"]) * 40
    score += data["relative_strength"] * 30

    return score

def classify(score):
    if score > 60:
        return "BUY"
    elif score < 40:
        return "SELL"
    return "HOLD"

def load_data(symbol: str):
    """
    select most current 20 specific stock prices
    :param symbol: stock symbol
    :return: object {"prices": list[stock prices], "relative_strength": number calculated by relative_strength(stock_return, gold_return)}
    """
    db = SessionLocal()

    try:
        stock_prices = db.scalars(
            select(StockPrice.price)
            .where(StockPrice.symbol == symbol,
                   StockPrice.price.is_not(None))
            .order_by(desc(StockPrice.timestamp))
            .limit(window_width)
        ).all()

        gold_prices = db.scalars(
            select(MetalPrice.price)
            .where(
                MetalPrice.metal == "XAU",
                MetalPrice.currency == "AUD",
                MetalPrice.price.is_not(None),
            )
            .order_by(desc(MetalPrice.timestamp))
            .limit(window_width)
        ).all()
    finally:
        db.close()

    if len(stock_prices) < window_width:
        raise ValueError(f"Not enough stock price history for {symbol}. Expected {window_width} rows, found {len(stock_prices)}.")

    if len(gold_prices) < 2:
        raise ValueError(f"Not enough gold price history to compute relative strength. Found {len(gold_prices)} rows.")

    prices = list(reversed(stock_prices))
    gold_series = list(reversed(gold_prices))

    stock_return = (prices[-1] - prices[0]) / prices[0]
    gold_return = (gold_series[-1] - gold_series[0]) / gold_series[0]

    return {
        "prices": prices,
        "relative_strength": relative_strength(stock_return, gold_return),
    }
