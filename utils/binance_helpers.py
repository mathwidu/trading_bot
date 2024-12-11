from binance.client import Client
import csv
import os
from datetime import datetime

def get_tickers(client: Client):
    """
    Retorna os preços de todas as criptomoedas disponíveis na Binance.
    """
    try:
        tickers = client.get_all_tickers()
        return tickers
    except Exception as e:
        print(f"Erro ao buscar tickers: {e}")
        return []

def log_tickers(tickers, log_file_path="data/logs/price_log.csv"):
    """
    Registra os preços das criptomoedas em um arquivo CSV.
    
    :param tickers: Lista de dicionários com informações de preços.
    :param log_file_path: Caminho para o arquivo de log.
    """
    try:
        # Verifica se o arquivo já existe
        file_exists = os.path.isfile(log_file_path)
        
        # Abre o arquivo no modo de adição
        with open(log_file_path, mode='a', newline='') as log_file:
            writer = csv.writer(log_file)
            
            # Escreve o cabeçalho se o arquivo for novo
            if not file_exists:
                writer.writerow(["timestamp", "symbol", "price"])
            
            # Escreve os dados
            for ticker in tickers:
                writer.writerow([datetime.now().isoformat(), ticker["symbol"], ticker["price"]])
        print(f"Dados registrados em {log_file_path}.")
    except Exception as e:
        print(f"Erro ao registrar dados: {e}")
