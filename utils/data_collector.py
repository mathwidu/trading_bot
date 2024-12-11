from binance.client import Client
import csv
from datetime import datetime

def get_historical_data(client: Client, symbol: str, interval: str, limit: int):
    """
    Busca dados históricos de velas (candlesticks) da Binance.

    Args:
        client (Client): Cliente da Binance.
        symbol (str): Par de criptomoedas (ex.: BTCUSDT).
        interval (str): Intervalo das velas (ex.: '1m', '1h', '1d').
        limit (int): Número de velas a buscar.

    Returns:
        list: Lista de dicionários com dados históricos.
    """
    try:
        # Obtendo dados históricos
        candles = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        historical_data = []

        for candle in candles:
            data = {
                'timestamp': datetime.utcfromtimestamp(candle[0] / 1000).isoformat(),
                'symbol': symbol,
                'price': candle[4]  # Preço de fechamento
            }
            historical_data.append(data)

        return historical_data
    except Exception as e:
        print(f"Erro ao buscar dados históricos: {e}")
        return []

def save_historical_data_to_csv(data, file_path):
    """
    Salva dados históricos no arquivo CSV.

    Args:
        data (list): Lista de dicionários com dados históricos.
        file_path (str): Caminho do arquivo CSV.
    """
    try:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow([row['timestamp'], row['symbol'], row['price']])
        print(f"Dados históricos salvos em {file_path}.")
    except Exception as e:
        print(f"Erro ao salvar dados no arquivo CSV: {e}")

# Exemplo de uso
if __name__ == "__main__":
    API_KEY = 'SUA_API_KEY'
    API_SECRET = 'SEU_API_SECRET'
    client = Client(API_KEY, API_SECRET)

    # Configurações
    SYMBOL = 'BTCUSDT'
    INTERVAL = '1h'  # Dados históricos de 1 hora
    LIMIT = 100  # Quantidade de velas

    FILE_PATH = './data/historical/historical_data.csv'

    # Obtendo dados históricos
    historical_data = get_historical_data(client, SYMBOL, INTERVAL, LIMIT)

    # Salvando dados no CSV
    save_historical_data_to_csv(historical_data, FILE_PATH)
