from core.db import SessionLocal
from models.metal_price import MetalPrice
from models.stock_price import StockPrice
from sqlalchemy import desc, select

window_width = 20
score_min = -100.0
score_max = 100.0

import numpy as np

def volatility(returns):
    return np.std(returns)

'''
How strongly the stock reacts to gold price.
'''
def gold_beta(stock_returns, gold_returns):
    # simplified covariance / variance
    covariance = np.cov(stock_returns, gold_returns)[0, 1]
    variance = np.var(gold_returns)
    if variance == 0:
        return 0.0
    return covariance / variance


def relative_strength(stock_return, gold_return):
    return stock_return - gold_return

def momentum(prices):
    w = window_width // 2
    return (prices[-1] - prices[-w]) / prices[-w]

def liquidity(volume_series):
    return sum(volume_series[-window_width:]) / window_width

def compute_score(factors):
    score = 0

    score += factors["gold_beta"] * 25
    score += factors["relative_strength"] * 25
    score += factors["momentum"] * 25
    score -= factors["volatility"] * 15
    score += factors["liquidity"] * 10

    return score

def classify(score):
    if score is None or np.isnan(score):
        return "HOLD"

    if score >= 65:
        return "BUY"
    if score <= 35:
        return "SELL"
    return "HOLD"

def normalize(score, min_s, max_s):
    if score is None or np.isnan(score):
        return 50.0
    if max_s == min_s:
        return 50.0

    normalized = 100 * (score - min_s) / (max_s - min_s)
    return max(0.0, min(100.0, normalized))


def load_data(symbol: str):
    """
    select most current 20 specific stock prices
    :param symbol: stock symbol
    :return:
    """
    db = SessionLocal()

    try:
        stock_rows = db.execute(
            select(StockPrice.price, StockPrice.volume)
            .where(
                StockPrice.symbol == symbol,
                StockPrice.price.is_not(None),
                StockPrice.volume.is_not(None),
            )
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

    if len(stock_rows) < window_width:
        raise ValueError(
            f"Not enough stock price history for {symbol}. Expected {window_width} rows, found {len(stock_rows)}."
        )

    if len(gold_prices) < window_width:
        raise ValueError(
            f"Not enough gold price history to compute factors. Expected {window_width} rows, found {len(gold_prices)}."
        )

    stock_prices = [float(price) for price, _ in stock_rows]
    volume_series = [int(volume) for _, volume in stock_rows]

    stock_returns = [
        (stock_prices[i] - stock_prices[i + 1]) / stock_prices[i + 1]
        for i in range(0, len(stock_prices)-1)
    ]
    gold_returns = [
        (gold_prices[i] - gold_prices[i + 1]) / gold_prices[i + 1]
        for i in range(0, len(gold_prices)-1)
    ]

    stock_return = (stock_prices[0] - stock_prices[-1]) / stock_prices[-1]
    gold_return = (gold_prices[0] - gold_prices[-1]) / gold_prices[-1]

    return {
        "relative_strength": relative_strength(stock_return, gold_return),
        "momentum": momentum(stock_prices),
        "gold_beta": gold_beta(stock_returns, gold_returns),
        "volatility": volatility(stock_returns),
        "liquidity": liquidity(volume_series),
    }
