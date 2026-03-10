# 📈 AI Stock Signal Prediction & Alert System
This project is a **FastAPI-based backend** that predicts stock trading signals using a **Machine Learning model** and provides **real-time stock data, backtesting, and email alerts**.
The system fetches stock data from Yahoo Finance, performs feature engineering, generates predictions using trained models, and sends alerts when price thresholds or buy signals occur.
# 🚀 Features
- 📊 **Stock Signal Prediction**
-   - Predict BUY / HOLD / SELL signals using trained ML models.
- 📉 **Backtesting Engine**
  - Evaluate trading strategy performance against market returns.
- 📡 **Live Stock Data**
  - Fetch real-time data from Yahoo Finance.
- 📧 **Automated Email Alerts**
  - Sends alerts when:
  - Price crosses threshold
  - ML model predicts BUY signal.
- 🔄 **Automated Scheduler**
  - Runs alerts every 5 minutes using APScheduler.
- 🌐 **REST API**
  - FastAPI endpoints for frontend integration.
- ☁️ **Cloud Deployment**
  - Deployable on **Render Cloud**.
---

# 🧠 Tech Stack

### Backend
- FastAPI
- Python

### Machine Learning
- Scikit-learn
- Pandas
- NumPy

### Data Source
- Yahoo Finance (yfinance)

### Scheduler
- APScheduler

### Deployment
- Render Cloud

---

# 📁 Project Structure



FASTAPI/

│

├── app/

│

│ ├── api/

│ │ └── routes.py

│ │

│ ├── alerts/

│ │ ├── alert_engine.py

│ │ └── email_service.py

│ │

│ ├── services/

│ │ ├── data_fetch.py

│ │ ├── data_clean.py

│ │ ├── data_features.py

│ │ ├── data_models.py

│ │ └── backtest_strategy.py

│ 

│ └── main.py


│
######├── models/

######│ ├── AAPL_model.pkl
######│ ├── AAPL_scaler.pkl
######│ └── AAPL_features.pkl
│

├── run_alerts.py

├── requirements.txt

├── render.yaml

└── README.md

---

# ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/stock-ai-backend.git
cd FASTAPI
2️⃣ Create Virtual Environment
python -m venv venv

Activate environment:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
▶️ Run FastAPI Server
uvicorn app.main:app --reload

API will run at:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs
⏰ Run Alert Scheduler
python run_alerts.py

The system will check alerts every 5 minutes.

📡 API Endpoints
GET /

Code location
app/main.py

Example request

http://127.0.0.1:8000/

Response

{
  "message": "Stock Signal Backend Running"
}

Purpose
✔ Check if backend is running.

2️⃣ Test Ticker Endpoint

Path

GET /test-ticker?ticker=AAPL

Code location
app/main.py

Example

http://127.0.0.1:8000/test-ticker?ticker=AAPL

Response example

{
  "ticker": "AAPL",
  "rows_fetched": 252,
  "columns": [
    "Date",
    "Close",
    "Volume",
    "Return",
    "MA20",
    "MA50",
    "Volatility",
    "Volume_Change",
    "RSI"
  ]
}

Purpose
✔ Validate ticker
✔ Verify data fetch + feature engineering.

3️⃣ Get Processed Stock Data

Path

GET /stock/{symbol}

Code location
app/main.py

Example

http://127.0.0.1:8000/stock/AAPL

Response example

[
  {
    "Date": "2026-03-05",
    "Close": 189.22,
    "Volume": 54300000,
    "Return": 0.004,
    "MA20": 187.9,
    "MA50": 182.3,
    "Volatility": 0.012,
    "Volume_Change": -0.03,
    "RSI": 61.4
  }
]

Purpose
✔ Returns latest processed stock data.
📌 Endpoints in routes.py
These are included using:
app.include_router(router)
File:
app/api/routes.py
4️⃣ Predict Trading Signal
Path
GET /signal/{ticker}
Example
http://127.0.0.1:8000/signal/AAPL

Response

{
  "ticker": "AAPL",
  "signal": "BUY",
  "price": 192.45
}

Purpose
✔ Uses ML model to predict signal.

Flow

API
 ↓
predict_signal()
 ↓
load_model
 ↓
fetch_stock_data
 ↓
feature_engineering
 ↓
model prediction
5️⃣ Backtest Trading Strategy

Path

GET /backtest/{symbol}

Example

http://127.0.0.1:8000/backtest/AAPL

Response

{
  "ticker": "AAPL",
  "market_return_%": 12.5,
  "strategy_return_%": 18.3,
  "outperformance_%": 5.8,
  "sharpe_ratio": 1.34,
  "max_drawdown_%": -7.2,
  "win_rate_%": 61.5
}

Purpose
✔ Compare ML strategy vs market.

📊 Total Endpoints in Your Project
Endpoint	Method	Purpose
/	GET	Backend status
/test-ticker	GET	Validate stock ticker
/stock/{symbol}	GET	Get processed stock data
/signal/{ticker}	GET	ML trading signal
/backtest/{symbol}	GET	Strategy performance

Total:
5 API endpoints
🔎 Swagger API Documentation

FastAPI automatically generates API docs.

Open:

http://127.0.0.1:8000/docs

You will see:

✔ All endpoints
✔ Test interface
✔ Request/response schemas
☁️ Deploying on Render
Create a render.yaml file in project root.
Example:
services:
  - type: web
    name: stock-fastapi-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port 10000

  - type: worker
    name: stock-alert-worker
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python run_alerts.py

🔐 Environment Variables
Set in Render dashboard:
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

🔗 Frontend Integration
Example React API call:
const BASE_URL = "https://your-api.onrender.com";
fetch(`${BASE_URL}/signal/AAPL`)
  .then(res => res.json())
  .then(data => console.log(data));

📊 Future Improvements
User dashboard
Live stock charts
Database for storing alerts
Real-time WebSocket updates
Automatic model retraining
Portfolio optimization

👨‍💻 Author
Karishma K
AI / ML + Full Stack Development
📜 License
This project is for educational and research purposes only. Stock predictions are not financial advice.
