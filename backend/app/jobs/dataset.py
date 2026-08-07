from pathlib import Path

import pandas as pd
import yfinance as yf


def ticker_list() -> list[str]:
    dataset_path = Path(__file__).with_name("ASX_Listed.csv")
    data = pd.read_csv(dataset_path, usecols=["ASX code", "GICs industry group"])

    materials = data.loc[
        data["GICs industry group"].eq("Materials"),
        "ASX code",
    ]

    return materials.dropna().astype(str).str.strip().tolist()

if __name__ == '__main__':
    # 1. Define your ASX tickers (using the .AX suffix required by Yahoo)
    # For a full automated database, you can scrape an active ticker list from Market Index first.
    asx_tickers = ["VAL","MM8","MI6","4DX","BC8", "WTM"]

    # 2. Set your data window
    start_date = "2010-01-01"
    end_date = "2026-02-01"

    # 3. Establish your HDF5 Storage file (using PyTables compression)
    hdf_file_path = "asx_prices_database.h5"

    with pd.HDFStore(
            hdf_file_path, mode="a", complevel=9, complib="blosc"
    ) as store:
        for ticker in asx_tickers:
            try:
                print(f"Exporting historical data for {ticker}...")

                # Fetch the data into a Pandas DataFrame
                df = yf.download(ticker+".AX", start=start_date, end=end_date)

                if not df.empty:
                    # Format index to ensure clean timestamp handling in HDF5
                    df.index = pd.to_datetime(df.index)

                    # Clean up ticker string for HDF5 group compatibility (removing the dot)
                    clean_key = ticker.replace(".", "_")

                    # Store the DataFrame inside the HDF5 file
                    store.put(clean_key, df, format="table", data_columns=True)

            except Exception as e:
                print(f"Failed to export {ticker}: {e}")

    print(f"\nSuccess! Your ASX prices are saved to: {hdf_file_path}")
