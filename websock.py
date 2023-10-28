import asyncio
import json
import httpx
from websockets import connect
from klines import create_candle_df, create_kline_snapshot_df, update_snapshot
from pprint import pprint
from indicators import get_pct_B


BASE_URL = "https://fapi.binance.com"
BASE_WS_URL = 'wss://fstream.binance.com'

def get_klines_snapshot(symbol:str, interval:str, limit:int=1_000) -> list:
    url = f"/fapi/v1/klines"
    params = {
        'symbol': symbol.lower(),
        'limit': limit,
        'interval': interval
    }
    resp = httpx.get(BASE_URL+url, params=params)
    
    return resp.json()


async def kline_socket(symbol:str, interval:str):
    snapshot = get_klines_snapshot(symbol, interval)
    snapshot = create_kline_snapshot_df(snapshot)
    snapshot["%B"] = get_pct_B(snapshot['close'])
    
    subscribe_msg = {
            "method": "SUBSCRIBE",
            "params": [
                f"{symbol.lower()}@kline_{interval}",
                ],
            "id": 1
            }

    async with connect(BASE_WS_URL + "/ws") as ws:
        await ws.send(json.dumps(subscribe_msg))
        while True:
            msg = json.loads(await ws.recv())
            if "e" in msg:
                candle = {
                    'open_time': msg['k']['t'],
                    'open': msg['k']['o'],
                    'close': msg['k']['c'],
                    'high': msg['k']['h'],
                    'low': msg['k']['l'],
                    'volume': msg['k']['v']
                }
                # creamos dataframe de la vela
                candle_df = create_candle_df(candle)
                
                # actualizamos snapshot si la vela cierra
                if msg["k"]["x"]:
                    snapshot = update_snapshot(snapshot, candle_df)
                    snapshot["%B"] = get_pct_B(snapshot['close'])
                
                # si la vela no cierra, lo que haremos es actualizar una copia
                # del snapshot y analizamos para saber si %B quiere salir de
                # bandas, al final la copia del sanpshot se le elimina la ùltima fila
                snap_copy = snapshot.copy()
                snap_copy = update_snapshot(snap_copy, candle_df)
                
                snap_copy["%B"] = get_pct_B(snap_copy['close'])
                print(snap_copy)
                
                snap_copy = snap_copy.iloc[:-1]