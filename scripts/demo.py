import yfinance as yf

if __name__ == '__main__':

    # 'TIO=F' is the ticker for Iron Ore 62% Fe, CFR China (Futures)
    ticker_symbol = "TIO=F"
    iron_ore = yf.Ticker(ticker_symbol)

    # Get data for the last 5 days to ensure at least 2 trading days are captured
    hist = iron_ore.history(period="5d")

    if not hist.empty and len(hist) >= 2:
        # Get last two rows
        latest_day = hist.iloc[-1]
        prev_day = hist.iloc[-2]

        # Values
        current_price = latest_day['Close']
        prev_close = prev_day['Close']

        # Calculations
        change = current_price - prev_close
        pct_change = (change / prev_close) * 100

        print(f"Ticker: {ticker_symbol}")
        print(f"Current Price: ${current_price:.2f} per ton")
        print(f"Daily Change: ${change:.2f}")
        print(f"Percent Change: {pct_change:.2f}%")
    else:
        print("Market data for Iron Ore is currently unavailable.")

