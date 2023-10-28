import asyncio
import pandas as pd
import math
from decimal import Decimal
from pprint import pprint

from shock_points import get_shock_points
from websock import kline_socket

async def main():
    # moneda a revisar
    symbol = "lqtyusdt"
    interval1 = Decimal('0.1')
    interval2 = Decimal('0.01')
    precision = 4
    
    await kline_socket(symbol,'5m')
    
    '''
    # Obtener el promedio entre los valores de los máximos de i1 en DataFramde de i2
    sp = await get_shock_points(precision, symbol=symbol, 
                                interval1=interval1, interval2=interval2)
    sp['symbol'] = symbol
    pprint(sp)'''
    


if __name__ == '__main__':
    asyncio.run(main())