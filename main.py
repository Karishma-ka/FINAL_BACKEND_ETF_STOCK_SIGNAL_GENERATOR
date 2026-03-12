from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.data_fetch import fetch_stock_data
from app.services.data_clean import clean_data
from app.services.data_features import add_features
from app.services.data_models import predict_signal
from app.api.routes import router
import logging

# ✅ Create FastAPI app
app = FastAPI()

# Allowed frontend origins
origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]


# ✅ Add CORS middleware HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")


@app.get("/")
def home():
    return {"message": "Stock Signal Backend Running"}


# Include API routes
app.include_router(router)


@app.get("/test-ticker")
def test_ticker(ticker: str):
    """
    Test whether a ticker is valid and data can be fetched
    """
    try:
        df = fetch_stock_data(ticker)
        df = clean_data(df)
        features = add_features(df)

        return {
            "ticker": ticker,
            "rows_fetched": len(df),
            "columns": list(features.columns)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stock/{symbol}")
def get_stock_data(symbol: str):
    try:
        df = fetch_stock_data(symbol)
        df = clean_data(df)
        df = add_features(df)

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No processed data available for symbol: {symbol}"
            )

        if "Date" in df.columns:
            df["Date"] = df["Date"].astype(str)

        return df.tail(5).to_dict(orient="records")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
