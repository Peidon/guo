import yfinance as yf

# Define the tickers
tickers = ['GDR.AX', 'GGR', 'LNQ.AX']

if __name__ == '__main__':

    # Fetch last close data for all tickers
    data = yf.download(tickers, period="1d", interval="1m", group_by='ticker')

    # Display last close for each
    for ticker in tickers:
        try:
            # Access the closing price from the DataFrame
            last_price = data[ticker]['Close'].iloc[-1]
            print(f"{ticker} Last Price: {last_price:.2f}")
        except KeyError:
            print(f"Data for {ticker} not found.")

    # Alternatively, for full info on a specific ticker:
    # info = yf.Ticker("GGR").info
    # print(info['currentPrice'])