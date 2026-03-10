import os
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

RAW_DATA_FILE = os.path.join(BASE_DIR, "data", "btc_usd_raw.csv")
PROCESSED_DATA_FILE = os.path.join(BASE_DIR, "data", "btc_usd_processed.csv")


# ---------------------------------------------------------
# Load Raw Data
# ---------------------------------------------------------

def load_raw_data():

    print("Loading raw dataset...")

    df = pd.read_csv(RAW_DATA_FILE)

    return df


# ---------------------------------------------------------
# Clean Dataset
# ---------------------------------------------------------

def clean_dataset(df):

    print("Cleaning dataset...")

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Sort dataset
    df = df.sort_values("date")

    # Reset index
    df = df.reset_index(drop=True)

    # Remove missing values
    df = df.dropna()

    return df


# ---------------------------------------------------------
# Save Processed Dataset
# ---------------------------------------------------------

def save_processed_dataset(df):

    df.to_csv(PROCESSED_DATA_FILE, index=False)

    print("Processed dataset saved to:", PROCESSED_DATA_FILE)


# ---------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------

def run_preprocessing_pipeline():

    df = load_raw_data()

    df = clean_dataset(df)

    save_processed_dataset(df)

    print("Data preprocessing completed successfully.")


# ---------------------------------------------------------
# Script Entry
# ---------------------------------------------------------

if __name__ == "__main__":
    run_preprocessing_pipeline()