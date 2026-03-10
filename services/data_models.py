import os
import pickle
from app.services.data_fetch import fetch_stock_data
from app.services.data_clean import clean_data
from app.services.data_features import add_features

# 🔹 Absolute path to models directory (SAFE)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")


def load_artifacts(ticker: str):
    model_path = os.path.join(MODEL_DIR, f"{ticker}_model.pkl")
    scaler_path = os.path.join(MODEL_DIR, f"{ticker}_scaler.pkl")
    features_path = os.path.join(MODEL_DIR, f"{ticker}_features.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file missing for {ticker}")

    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file missing for {ticker}")

    if not os.path.exists(features_path):
        raise FileNotFoundError(f"Feature file missing for {ticker}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    with open(features_path, "rb") as f:
        features = pickle.load(f)

    return model, scaler, features


def predict_signal(ticker: str):
    # 🔹 Load trained artifacts
    model, scaler, features = load_artifacts(ticker)

    # 🔹 Fetch & process data
    df = fetch_stock_data(ticker)
    df = clean_data(df)
    df = add_features(df)

    if df.empty:
        raise ValueError("No data available after feature engineering")

    # 🔹 Validate feature consistency
    missing = set(features) - set(df.columns)
    if missing:
        raise ValueError(f"Missing features in live data: {missing}")

    # 🔹 Use latest row for prediction
    latest = df[features].iloc[-1:]
    latest_scaled = scaler.transform(latest)

    # 🔹 Predict signal
    pred = model.predict(latest_scaled)[0]
    signal_map = {1: "BUY", 0: "HOLD", -1: "SELL"}

    return {
        "ticker": ticker,
        "signal": signal_map[int(pred)],
        "price": float(df["Close"].iloc[-1])
    }
