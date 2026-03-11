from __future__ import annotations

import os

import pandas as pd
import requests
import yfinance as yf


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "btc_usd_raw.csv")

BINANCE_API = "https://api.binance.com/api/v3/klines"
YFINANCE_SYMBOL = "BTC-USD"

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

def _normalize_dataset(df):

    if df.empty:
        raise ValueError("No BTC market data was returned by the upstream provider.")

    expected_columns = ["date", "open", "high", "low", "close", "volume"]
    frame = df[expected_columns].copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.astype(
        {
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": float,
        }
    )
    frame = frame.sort_values("date").dropna().reset_index(drop=True)
    print(f"Downloaded {len(frame)} rows.")
    return frame


def download_from_binance():

    print("Downloading BTC historical data from Binance...")

    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": LIMIT
    }

    response = requests.get(BINANCE_API, params=params, timeout=30)

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
    return _normalize_dataset(df)


def download_from_yfinance():

    print("Falling back to Yahoo Finance for BTC historical data...")
    ticker = yf.Ticker(YFINANCE_SYMBOL)
    history = ticker.history(period="max", interval="1d", auto_adjust=False)
    if history.empty:
        raise ValueError("Yahoo Finance returned an empty BTC-USD history.")

    history = history.reset_index().rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )
    return _normalize_dataset(history)


def load_cached_dataset():

    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError("No cached BTC dataset is available.")

    print("Using cached BTC dataset from disk.")
    return _normalize_dataset(pd.read_csv(DATA_FILE))


def download_btc_data():

    providers = [download_from_binance, download_from_yfinance]
    last_error = None

    for provider in providers:
        try:
            return provider()
        except Exception as exc:
            last_error = exc
            print(f"{provider.__name__} failed: {exc}")

    try:
        return load_cached_dataset()
    except Exception:
        pass

    raise RuntimeError("All BTC data sources failed.") from last_error


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
