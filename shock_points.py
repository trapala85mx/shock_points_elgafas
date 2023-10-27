import asyncio
import pandas as pd
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


async def get_shock_points(asks_df:pd.DataFrame, bids_df:pd.DataFrame, 
                           ask_max_prices:list[float], bid_max_prices,
                           precision:int):
    
    tasks = []
    tasks.append(get_ask_shock_points(asks_df, ask_max_prices, precision))
    tasks.append(get_bid_shock_points(bids_df, bid_max_prices, precision))
    
    asks_sp , bids_sp = await asyncio.gather(*tasks)
    
    return {
            'asks_max_prices': ask_max_prices,
            'asks_sp': asks_sp,
            'bids_max_prices': bid_max_prices,
            'bids_sp': bids_sp
        }