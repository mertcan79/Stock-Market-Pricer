from fastapi import FastAPI, Body
from typing import Dict
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import utils
from models import Payload

def start_application():
    app = FastAPI(title='MertcanCoskun', version='1.0.0')
    return app


app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
async def main_logic(request_data: Payload) -> Dict:

    stock_info = {}

    symbol = request_data.symbol
    currency = request_data.currency
    dates = request_data.dates

    daily_close = utils.main(ticker=symbol, dates=dates, convert_to=currency)

    stock_info['symbol'] = symbol
    stock_info['currency'] = currency
    stock_info["daily_close"] = daily_close

    return stock_info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, log_level="debug")

