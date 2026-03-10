import os
import requests
import pandas as pd
from datetime import datetime


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "btc_usd_raw.csv")

BINANCE_API = "https://api.binance.com/api/v3/klines"

SYMBOL = "BTCUSDT"
INTERVAL = "1d"
LIMIT = 1000


# ---------------------------------------------------------
# Ensure data directory exists
# ---------------------------------------------------------

def ensure_data_directory():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


# ---------------------------------------------------------
# Download BTC Data from Binance
# ---------------------------------------------------------

def download_btc_data():

    print("Downloading BTC historical data from Binance...")

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": LIMIT
    }

    response = requests.get(BINANCE_API, params=params)

    if response.status_code != 200:
        raise ValueError("Failed to fetch data from Binance API")

    data = response.json()

    columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore"
    ]

    df = pd.DataFrame(data, columns=columns)

    df["date"] = pd.to_datetime(df["open_time"], unit="ms")

    df = df[["date", "open", "high", "low", "close", "volume"]]

    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })

    print(f"Downloaded {len(df)} rows.")

    return df


# ---------------------------------------------------------
# Save Dataset
# ---------------------------------------------------------

def save_dataset(df):

    df.to_csv(DATA_FILE, index=False)

    print("Dataset saved to:", DATA_FILE)


# ---------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------

def run_ingestion_pipeline():

    ensure_data_directory()

    df = download_btc_data()

    save_dataset(df)

    print("Data ingestion pipeline completed successfully.")


# ---------------------------------------------------------
# Script Entry
# ---------------------------------------------------------

if __name__ == "__main__":
    run_ingestion_pipeline()