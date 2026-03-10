import os
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

INPUT_FILE = os.path.join(BASE_DIR, "data", "btc_usd_processed.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "btc_usd_features.csv")


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

def load_dataset():

    print("Loading processed dataset...")

    df = pd.read_csv(INPUT_FILE)

    return df


# ---------------------------------------------------------
# Generate Features
# ---------------------------------------------------------

def generate_features(df):

    print("Generating features...")

    # Moving averages
    df["ma_7"] = df["close"].rolling(window=7).mean()
    df["ma_30"] = df["close"].rolling(window=30).mean()

    # Volatility
    df["volatility"] = df["close"].rolling(window=7).std()

    # Lag features
    df["lag_1"] = df["close"].shift(1)
    df["lag_7"] = df["close"].shift(7)

    # Daily returns
    df["return"] = df["close"].pct_change()

    # Remove NaN rows created by rolling calculations
    df = df.dropna()

    return df


# ---------------------------------------------------------
# Save Feature Dataset
# ---------------------------------------------------------

def save_features(df):

    df.to_csv(OUTPUT_FILE, index=False)

    print("Feature dataset saved to:", OUTPUT_FILE)


# ---------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------

def run_feature_pipeline():

    df = load_dataset()

    df = generate_features(df)

    save_features(df)

    print("Feature engineering completed successfully.")


# ---------------------------------------------------------
# Script Entry
# ---------------------------------------------------------

if __name__ == "__main__":
    run_feature_pipeline()