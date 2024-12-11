import pandas as pd

def calculate_sma(data: pd.DataFrame, period: int) -> pd.Series:
    """
    Calcula a Média Móvel Simples (SMA).
    
    :param data: DataFrame contendo os preços históricos.
    :param period: Número de períodos para o cálculo da SMA.
    :return: Série com os valores da SMA.
    """
    return data['close'].rolling(window=period).mean()

def calculate_ema(data: pd.DataFrame, period: int) -> pd.Series:
    """
    Calcula a Média Móvel Exponencial (EMA).
    
    :param data: DataFrame contendo os preços históricos.
    :param period: Número de períodos para o cálculo da EMA.
    :return: Série com os valores da EMA.
    """
    return data['close'].ewm(span=period, adjust=False).mean()
