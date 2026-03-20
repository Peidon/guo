import yfinance as yf

def fetch_stock_price(symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")

    if data.empty:
        return None

    latest = data.iloc[-1]

    return {
        "symbol": symbol,
        "price": float(latest["Close"]),
        "volume": int(latest["Volume"]),
        "timestamp": latest.name.to_pydatetime()
    }