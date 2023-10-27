import httpx
import pandas as pd


BASE = "https://fapi.binance.com"
WS_BASE = "wss://fstream.binance.com/ws"


def get_order_book_snapshot(symbol: str, limit: int = 1_000) -> dict:
    global BASE
    url = "/fapi/v1/depth"
    params = {
        'symbol':symbol.lower(),
        'limit': limit
    }
    try:
        resp = httpx.get(url=BASE+url, params=params)
    
    except httpx._exceptions.RequestError as e:
        print(e)
    
    except Exception as e:
        print(e)
    else:
        return resp.json()


async def create_df(snapshot: dict, side:str) -> pd.DataFrame:
    df = pd.DataFrame(snapshot, columns=['price', 'qty'], dtype=float)
    return df


async def get_mean(minim:float, maxim:float, df:pd.DataFrame, precision:int) -> float:
    df = df[(df.price>=minim) & (df.price<=maxim)]
    weighted_mean = (df['quantity'] * df['price']).sum() / df['quantity'].sum()
    
    return round(weighted_mean, precision)