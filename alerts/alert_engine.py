import numpy as np
from app.services.data_fetch import fetch_stock_data
from app.services.data_clean import clean_data
from app.services.data_features import add_features
from app.services.data_models import load_artifacts
from app.alerts.email_service import send_email_alert


def check_alerts(ticker: str, threshold_price: float, user_email: str):

    try:

        print(f"Checking alerts for {ticker}")

        model, scaler, features = load_artifacts(ticker)

        if model is None or scaler is None or features is None:
            print(f"No trained model found for {ticker}")
            return

        # Fetch and process data
        df = fetch_stock_data(ticker)
        df = clean_data(df)
        df = add_features(df)

        if df.empty:
            print("No data available")
            return

        latest_price = df["Close"].iloc[-1]

        print(f"{ticker} price: {latest_price}")

        # PRICE ALERT
        if latest_price >= threshold_price:

            message = f"""
PRICE ALERT

Ticker: {ticker}
Current Price: {latest_price}
Threshold: {threshold_price}
"""

            send_email_alert(
                subject=f"{ticker} Price Alert",
                message=message,
                to_email=user_email
            )

            print("Price alert sent")

        # MODEL FEATURES
        X = df[features]

        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.dropna()

        if X.empty:
            print("No valid feature data")
            return

        # Scale features
        X_scaled = scaler.transform(X)

        # Use latest row only
        latest_features = X_scaled[-1].reshape(1, -1)

        prediction = model.predict(latest_features)[0]

        print(f"{ticker} model prediction: {prediction}")

        # BUY SIGNAL
        if prediction == 1:

            message = f"""
BUY SIGNAL

Ticker: {ticker}
Current Price: {latest_price}
"""

            send_email_alert(
                subject=f"{ticker} BUY SIGNAL",
                message=message,
                to_email=user_email
            )

            print("BUY alert sent")

        # SELL SIGNAL
        elif prediction == -1:

            message = f"""
SELL SIGNAL

Ticker: {ticker}
Current Price: {latest_price}
"""

            send_email_alert(
                subject=f"{ticker} SELL SIGNAL",
                message=message,
                to_email=user_email
            )

            print("SELL alert sent")

        else:
            print("No trading signal")

    except Exception as e:
        print(f"Alert engine error: {e}")
