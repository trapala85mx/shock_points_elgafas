import asyncio
import pandas as pd
import math
from decimal import Decimal
from pprint import pprint
from utils import get_order_book_snapshot
from utils import create_df
from agg_level import agg_level
from agg_level import get_max_values
from shock_points import get_shock_points


async def main():
    # moneda a revisar
    symbol = "agldusdt"
    interval1 = Decimal('0.01')
    interval2 = Decimal('0.001')
    precision = 4
    
    # obtener la foto actual de libro
    snapshot = get_order_book_snapshot(symbol, 1_000)
    
    # Obtener los DataFrames de los asks y bids
    tasks = []
    tasks.append(create_df(snapshot['asks'], "asks"))
    tasks.append(create_df(snapshot['bids'], "bids"))
    asks_df, bids_df = await asyncio.gather(*tasks)
    
    # Obtener los asks y bids filtrados por mùltiplos
    asks_i1, bids_i1, asks_i2, bids_i2 = await agg_level(asks_df, bids_df, interval1, interval2)
    
    # Obtener màximos valores del primer intervalo
    asks_i1_max_prices, _ = await get_max_values(asks_i1)
    bids_i1_max_prices, _ = await get_max_values(bids_i1)
    
    # Obtener el promedio entre los valores de los máximos de i1 en DataFramde de i2
    sp = await get_shock_points(asks_i2, bids_i2, asks_i1_max_prices, bids_i1_max_prices, precision)
    pprint(sp)


if __name__ == '__main__':
    asyncio.run(main())