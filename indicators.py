import pandas as pd

def get_pct_B(close:pd.Series) -> pd.Series:
    # Calcula la media móvil y desviación estándar
    sma = close.rolling(window=20).mean()
    std = close.rolling(window=20).std()
    
    # Calcula las Bandas de Bollinger
    upper_band = sma + 2 * std
    lower_band = sma - 2 * std
    
    # Calcula el %B
    pct_B = ((close - lower_band) / (upper_band - lower_band)) * 100
    
    return round(pct_B/100,2)
