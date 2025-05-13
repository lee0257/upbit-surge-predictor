import asyncio
import json
import websockets
import requests
import time

TELEGRAM_TOKEN = "6437254217:AAF-oFmu6cRrBqEUZ5xwDb2cm7I0XAfdb9w"
TELEGRAM_CHAT_ID = "1901931119"
ALERT_INTERVAL = 1800

last_alert_time = {}
KRW_MARKET = []

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

def fetch_market_info():
    global KRW_MARKET
    url = "https://api.upbit.com/v1/market/all"
    res = requests.get(url).json()
    KRW_MARKET = [m for m in res if m['market'].startswith('KRW-') and m.get('market_warning') != 'CAUTION']

def is_surge_condition(data):
    try:
        market = data['code']
        now_price = float(data['trade_price'])
        acc_volume = float(data['acc_trade_price_24h'])
        ask_bid = data['ask_bid']
        if acc_volume < 500000000:
            return False
        now = time.time()
        if market in last_alert_time and now - last_alert_time[market] < ALERT_INTERVAL:
            return False
        if ask_bid == "BID":
            last_alert_time[market] = now
            return True
        return False
    except Exception as e:
        print("조건 체크 오류:", e)
        return False

def format_message(data):
    market = data['code']
    price = int(data['trade_price'])
    name = next((m['korean_name'] for m in KRW_MARKET if m['market'] == market), market)
    return f"[선행급등포착]\n- 코인명: {name}\n- 현재가: {price}원\n- 추천 이유: 매수세 유입 + 거래대금 기준 초과"

async def run():
    fetch_market_info()
    codes = [m['market'] for m in KRW_MARKET]
    url = "wss://api.upbit.com/websocket/v1"
    while True:
        try:
            async with websockets.connect(url) as ws:
                subscribe = [{"ticket": "test"}, {"type": "trade", "codes": codes}]
                await ws.send(json.dumps(subscribe))
                while True:
                    data = await ws.recv()
                    parsed = json.loads(data)
                    if is_surge_condition(parsed):
                        msg = format_message(parsed)
                        send_telegram_message(msg)
        except Exception as e:
            print("WebSocket 오류 발생:", e)
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(run())
