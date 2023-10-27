import asyncio
import math
import pandas as pd
from decimal import Decimal


async def agg_bid_level(df:pd.DataFrame, interval:Decimal):
    df['side'] = 'bid'
    min_bid_level = math.floor( min(df.price)/float(interval) ) * interval
    max_bid_level = ( math.ceil( max(df.price)/float(interval) ) + 1 ) * interval
    
    bid_level_bounds = [ float(min_bid_level + interval*x) for x in range( int((max_bid_level-min_bid_level)/interval) +1) ]
    
    df['bins'] = pd.cut(df.price, bins=bid_level_bounds, right=False, precision=10)
    
    df = df.groupby('bins', observed=False).agg(quantity=('qty','sum'), side=('side','first')).reset_index()
    
    df['price'] = df.bins.apply(lambda x:x.left)
    df.price = df.price.astype('float')
    
    df = df.drop('bins', axis=1)
    df = df.sort_values(by="price", ascending=False)
    df = df[df['quantity'] != 0]
    return df


async def agg_ask_level(df:pd.DataFrame, interval:Decimal):
    df['side'] = 'ask'
    min_ask_level = ( math.floor( min(df.price)/float(interval) ) -1 ) * interval
    max_ask_level = ( math.ceil( max(df.price)/float(interval) ) ) * interval
    
    ask_level_bounds = [ float(min_ask_level + interval*x) for x in range( int((max_ask_level-min_ask_level)/interval) +1) ]
    
    df['bins'] = pd.cut(df.price, bins=ask_level_bounds, right=True, precision=10)
    
    df = df.groupby('bins', observed=False).agg(quantity=('qty','sum'), side=('side', 'first')).reset_index()
    
    df['price'] = df.bins.apply(lambda x:x.right)
    df.price = df.price.astype('float')
    
    df = df.drop('bins', axis=1)
    df = df.sort_values(by="price", ascending=False)
    df = df[df['quantity'] != 0]
    
    return df


async def get_max_values(df:pd.DataFrame) -> list[float]:
    df = df.sort_values(by="quantity", ascending=False)
    df = df[:4]
    
    return sorted(df['price'].tolist()), sorted(df['quantity'].tolist())


async def agg_level(asks_df:pd.DataFrame, bids_df:pd.DataFrame, interval1:str, interval2:str) -> pd.DataFrame:
    tasks = []
    tasks.append(agg_ask_level(asks_df, Decimal(interval1)))
    tasks.append(agg_bid_level(bids_df, Decimal(interval1)))
    tasks.append(agg_ask_level(asks_df, Decimal(interval2)))
    tasks.append(agg_bid_level(bids_df, Decimal(interval2)))
    asks_i1, bids_i1, asks_i2, bids_i2 = await asyncio.gather(*tasks)
    return asks_i1, bids_i1, asks_i2, bids_i2