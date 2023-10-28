import pandas as pd


def create_candle_df(candle:dict) -> pd.DataFrame:
    df = pd.DataFrame([candle])
    df.open_time = pd.to_datetime(df.open_time, unit="ms")
    df.open = df.open.astype("float64")
    df.high = df.high.astype("float64")
    df.low = df.low.astype("float64")
    df.close = df.close.astype("float64")
    df.volume = df.volume.astype("float64")
    return df


def create_kline_snapshot_df(data:list[list]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df = df.iloc[:,:6]
    df = df.iloc[:-1]
    df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume']
    df.open_time = pd.to_datetime(df.open_time, unit="ms")
    df.open = df.open.astype("float64")
    df.high = df.high.astype("float64")
    df.low = df.low.astype("float64")
    df.close = df.close.astype("float64")
    df.volume = df.volume.astype("float64")
    return df


def update_snapshot(snap:pd.DataFrame, candle:pd.DataFrame) -> pd.DataFrame:
    return pd.concat([snap, candle], ignore_index=True)