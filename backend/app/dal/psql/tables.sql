CREATE TABLE metal_prices (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    metal VARCHAR(10) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    prev_close_price NUMERIC(15, 4) NOT NULL,
    open_price NUMERIC(15, 4) NOT NULL,
    low_price NUMERIC(15, 4) NOT NULL,
    high_price NUMERIC(15, 4) NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    price NUMERIC(15, 4) NOT NULL,
    ch NUMERIC(15, 4) NOT NULL,         -- Change (current price - open_price)
    chp NUMERIC(10, 4) NOT NULL,        -- Change percentage
    ask NUMERIC(15, 4) NOT NULL,
    bid NUMERIC(15, 4) NOT NULL,
    price_gram_24k NUMERIC(15, 4),
    price_gram_22k NUMERIC(15, 4),
    price_gram_21k NUMERIC(15, 4),
    price_gram_20k NUMERIC(15, 4),
    price_gram_18k NUMERIC(15, 4),
    price_gram_16k NUMERIC(15, 4),
    price_gram_14k NUMERIC(15, 4),
    price_gram_10k NUMERIC(15, 4)
);

CREATE INDEX idx_metal_symbol_time
ON metal_prices(symbol, timestamp DESC);

CREATE TABLE stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    price NUMERIC(15, 4),
    volume BIGINT,
    timestamp TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_stock_symbol_time
ON stock_prices(symbol, timestamp DESC);