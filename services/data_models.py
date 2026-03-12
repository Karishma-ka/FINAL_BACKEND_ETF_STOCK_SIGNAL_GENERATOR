import os
import pickle
from app.services.data_fetch import fetch_stock_data
from app.services.data_clean import clean_data
from app.services.data_features import add_features

# Absolute path to models directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")


def load_artifacts(ticker: str):

    model_path = os.path.join(MODEL_DIR, f"{ticker}_model.pkl")
    scaler_path = os.path.join(MODEL_DIR, f"{ticker}_scaler.pkl")
    features_path = os.path.join(MODEL_DIR, f"{ticker}_features.pkl")

    if not os.path.exists(model_path):
        print(f"⚠ Model file missing for {ticker}")
        return None, None, None

    try:

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)

        with open(features_path, "rb") as f:
            features = pickle.load(f)

        return model, scaler, features

    except Exception as e:
        print(f"Error loading artifacts for {ticker}: {e}")
        return None, None, None


def predict_signal(ticker: str):

    model, scaler, features = load_artifacts(ticker)

    if model is None:
        raise FileNotFoundError(f"No trained model available for {ticker}")

    # Fetch stock data
    df = fetch_stock_data(ticker)
    df = clean_data(df)
    df = add_features(df)

    if df.empty:
        raise ValueError("No data available after feature engineering")

    # Validate feature consistency
    missing = set(features) - set(df.columns)
    if missing:
        raise ValueError(f"Missing features in live data: {missing}")

    # Use latest row
    latest = df[features].iloc[-1:]
    latest_scaled = scaler.transform(latest)

    # Predict
    pred = model.predict(latest_scaled)[0]

    signal_map = {
        1: "BUY",
        0: "HOLD",
        -1: "SELL"
    }

    signal = signal_map.get(int(pred), "HOLD")

    return {
        "ticker": ticker,
        "signal": signal,
        "price": float(df["Close"].iloc[-1])
    }
