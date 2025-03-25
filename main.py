from binance.client import Client
from config.settings import API_KEY, API_SECRET
from utils.binance_helpers import get_tickers, log_tickers
from utils.data_collector import get_historical_data, save_historical_data_to_csv
from strategies.moving_averages import calculate_sma, calculate_ema
import pandas as pd
import numpy as np

# Configurando o cliente da Binance
client = Client(API_KEY, API_SECRET)

# Busca os preços das criptomoedas
tickers = get_tickers(client)
print(tickers[:5])  # Exibe os preços das 5 primeiras criptomoedas

# Registra os preços em um arquivo CSV
log_tickers(tickers)

# Configuração para buscar dados históricos
SYMBOL = 'BTCUSDT'  # Moeda para buscar dados históricos
INTERVAL = '1h'     # Intervalo dos dados
LIMIT = 100         # Número de registros históricos a buscar
FILE_PATH = './data/historical/historical_data.csv'

# Baixa e salva os dados históricos
historical_data = get_historical_data(client, SYMBOL, INTERVAL, LIMIT)
save_historical_data_to_csv(historical_data, FILE_PATH)

print(f"Dados históricos de {SYMBOL} salvos com sucesso em {FILE_PATH}!")

# Carregar os dados históricos para cálculo de médias móveis
data = pd.read_csv(FILE_PATH, names=['timestamp', 'symbol', 'close'])
data['close'] = data['close'].astype(float)

# Calcular médias móveis
data['SMA_5'] = calculate_sma(data, 5)
data['EMA_5'] = calculate_ema(data, 5)

# Gerar sinais de compra e venda com base no cruzamento SMA/EMA
data['Signal'] = np.where(
    (data['EMA_5'] > data['SMA_5']) & (data['EMA_5'].shift(1) <= data['SMA_5'].shift(1)), 1,
    np.where(
        (data['EMA_5'] < data['SMA_5']) & (data['EMA_5'].shift(1) >= data['SMA_5'].shift(1)), -1,
        0
    )
)

# Exibir últimas 10 linhas com médias e sinais
print("\nÚltimas 10 linhas com SMA, EMA e Sinais:")
print(data[['timestamp', 'close', 'SMA_5', 'EMA_5', 'Signal']].tail(10))

# Exibir sinais detectados
print("\nSINAIS DETECTADOS:")
for index, row in data.iterrows():
    if row['Signal'] == 1:
        print(f"{row['timestamp']}: SINAL DE COMPRA - Preço: {row['close']}")
    elif row['Signal'] == -1:
        print(f"{row['timestamp']}: SINAL DE VENDA - Preço: {row['close']}")
