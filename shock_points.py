import asyncio
import pandas as pd
from utils import get_order_book_snapshot
from utils import create_df
from agg_level import agg_level
from agg_level import get_max_values
from utils import get_mean


async def get_ask_shock_points(df:pd.DataFrame, max_values:list[float], precision:int) -> list[int]:
    tasks = []
    tasks.append(get_mean(max_values[0], max_values[1], df, precision))
    tasks.append(get_mean(max_values[1], max_values[2], df, precision))
    tasks.append(get_mean(max_values[2], max_values[3], df, precision))
    
    sp_ask_1 , sp_ask_2 , sp_ask_3 = await asyncio.gather(*tasks)
    
    return [sp_ask_1, sp_ask_2, sp_ask_3]


async def get_bid_shock_points(df:pd.DataFrame, max_values:list[float], precision:int) -> list[int]:
    tasks = []
    tasks.append(get_mean(max_values[0], max_values[1], df, precision))
    tasks.append(get_mean(max_values[1], max_values[2], df, precision))
    tasks.append(get_mean(max_values[2], max_values[3], df, precision))
    
    sp_bid_1 , sp_bid_2 , sp_bid_3 = await asyncio.gather(*tasks)
    
    return [sp_bid_1, sp_bid_2, sp_bid_3]


async def get_shock_points(precision:int, **kwargs):
    # obtener la foto actual de libro
    snapshot = get_order_book_snapshot(kwargs['symbol'], 1_000)
    
    # Obtener los DataFrames de los asks y bids
    tasks = []
    
    tasks.append(create_df(snapshot['asks'], "asks"))
    tasks.append(create_df(snapshot['bids'], "bids"))
    asks_df, bids_df = await asyncio.gather(*tasks)
    
    # Obtener los asks y bids filtrados por mùltiplos
    asks_i1, bids_i1, asks_df, bids_df = await agg_level(asks_df, bids_df, kwargs['interval1'], kwargs['interval2'])
    
    # Obtener màximos valores del primer intervalo
    ask_max_prices, _ = await get_max_values(asks_i1)
    bid_max_prices, _ = await get_max_values(bids_i1)
    
    tasks = []
    
    if len(ask_max_prices) == 4 and len(bid_max_prices) < 4:
        tasks.append(get_ask_shock_points(asks_df, ask_max_prices, precision))
        asks_sp = await asyncio.gather(*tasks)
        bids_sp = None
    
    elif len(ask_max_prices) < 4 and len(bid_max_prices) == 4:
        tasks.append(get_bid_shock_points(bids_df, bid_max_prices, precision))
        bids_sp = await asyncio.gather(*tasks)
        asks_sp = None
    
    elif len(ask_max_prices) == 4 and len(bid_max_prices) == 4:
        tasks.append(get_ask_shock_points(asks_df, ask_max_prices, precision))
        tasks.append(get_bid_shock_points(bids_df, bid_max_prices, precision))
        asks_sp , bids_sp = await asyncio.gather(*tasks)
    
    elif len(ask_max_prices) < 4 and len(bid_max_prices) < 4:
        asks_sp = None
        bids_sp = None
    
    return {
            'asks_max_prices': ask_max_prices,
            'asks_sp': asks_sp,
            'bids_max_prices': bid_max_prices,
            'bids_sp': bids_sp
        }