import json
import time
import requests

with open("config.json", "r") as f:
    config = json.load(f)

TELEGRAM_BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]

def get_json(url):
    return requests.get(url).json()

def get_tickers():
    url = "https://api.upbit.com/v1/market/all"
    return [x['market'] for x in get_json(url) if x['market'].startswith("KRW-")]

def get_price_data(ticker):
    url = f"https://api.upbit.com/v1/ticker?markets={ticker}"
    data = get_json(url)[0]
    return {
        "ticker": ticker,
        "trade_price": data['trade_price'],
        "acc_trade_price_24h": data['acc_trade_price_24h']
    }

def get_orderbook(ticker):
    url = f"https://api.upbit.com/v1/orderbook?markets={ticker}"
    return get_json(url)[0]

def detect_signals():
    results = []
    for ticker in get_tickers():
        data = get_price_data(ticker)
        ob = get_orderbook(ticker)
        buy_sum = sum([o['bid_size'] for o in ob['orderbook_units'][:5]])
        sell_sum = sum([o['ask_size'] for o in ob['orderbook_units'][:5]])
        ratio = buy_sum / (sell_sum + 1e-6)

        if data['acc_trade_price_24h'] > 1_200_000_000:
            if ratio > 1.5:
                results.append({
                    "coin": data['ticker'],
                    "price": data['trade_price'],
                    "buy_range": f"{int(data['trade_price']*0.995)} ~ {int(data['trade_price']*1.005)}",
                    "target": int(data['trade_price']*1.03),
                    "expect": "3% 이상",
                    "reason": "매수세 급증 + 호가 우위 포착"
                })
    return results

def send_telegram_message(signal):
    msg = f"""[선행급등포착]
- 코인명: {signal['coin']}
- 현재가: {signal['price']}원
- 매수 추천가: {signal['buy_range']}원
- 목표 매도가: {signal['target']}원
- 예상 수익률: {signal['expect']}
- 예상 소요 시간: 10분 내
- 추천 이유: {signal['reason']}"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=data)

if __name__ == "__main__":
    while True:
        try:
            signals = detect_signals()
            for signal in signals:
                send_telegram_message(signal)
            time.sleep(60)
        except Exception as e:
            print("[오류]", e)
            time.sleep(30)
