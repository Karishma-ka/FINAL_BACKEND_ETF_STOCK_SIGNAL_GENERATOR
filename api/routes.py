from fastapi import APIRouter, HTTPException
from app.services.data_models import predict_signal
from app.strategies.backtest_strategy import backtest_strategy

router = APIRouter()

@router.get("/signal/{ticker}")
def get_signal(ticker: str):
    try:
        return predict_signal(ticker)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/backtest/{symbol}")
def run_backtest(symbol: str):
    return backtest_strategy(symbol)
