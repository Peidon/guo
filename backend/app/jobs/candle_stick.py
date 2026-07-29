import yfinance as yf
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import HoverTool

if __name__ == '__main__':

    # 1. Fetch data for the last month (use '1mo' for one month of daily data)
    ticker = "VAL.AX"
    df = yf.download(ticker, period="1mo")

    # FIX: Flatten the yfinance MultiIndex columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Reset index to make 'Date' an accessible column
    df = df.reset_index()

    # 2. Categorise days into gains and losses (Now safely returns a 1D Series)
    inc = df['Close'] > df['Open']
    dec = df['Open'] > df['Close']

    # 12 hours in milliseconds for bar width configuration
    w = 12 * 60 * 60 * 1000

    # 3. Initialize the Bokeh plot
    p = figure(
        x_axis_type="datetime",
        title=f"{ticker} Candlestick Plot (Last 1 Month)",
        width=800,
        height=400,
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    p.grid.grid_line_alpha = 0.3

    # 4. Generate the wicks (high/low lines)
    p.segment(df['Date'], df['High'], df['Date'], df['Low'], color="black")

    # 5. Generate the bodies (green for gains, red for losses) using safe bracket notation
    # Increasing days
    p.vbar(
        df['Date'][inc], w, df['Open'][inc], df['Close'][inc],
        fill_color="#26a69a", line_color="#26a69a"
    )
    # Decreasing days
    p.vbar(
        df['Date'][dec], w, df['Open'][dec], df['Close'][dec],
        fill_color="#ef5350", line_color="#ef5350"
    )

    # 6. Configure interactive hover tools
    # hover = HoverTool(tooltips=[
    #     ("Date", "@x{%F}"),
    #     ("Open", "$@bottom{0.000}"),
    #     ("Close", "$@top{0.000}"),
    # ])
    # hover.formatters = {"@x": "datetime"}
    # p.add_tools(hover)

    # 7. Render plot in browser
    show(p)
