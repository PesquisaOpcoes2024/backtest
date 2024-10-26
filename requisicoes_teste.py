import pandas as pd
import mplfinance as mpl

# Carregar os dados de PETR4 do arquivo CSV (ou dos dados de opções processados)
df = pd.read_csv('options_data.csv')

# Verifique se os dados possuem as colunas corretas
print(df.head())  # Visualizar os dados para garantir que estão corretos

# Filtrar os dados e selecionar as colunas importantes
df_filtered = df[['open', 'high', 'low', 'close', 'volume']]

# Configurar a coluna de datas como índice
df_filtered['Date'] = pd.to_datetime(df['name'].apply(extract_expiration_date))  # Extraindo a data de vencimento
df_filtered.set_index('Date', inplace=True)

# Plotar os dados como gráfico de candlestick
mpl.plot(df_filtered, type='candle', volume=True, style='charles', title='Gráfico de Candlestick - PETR4', ylabel='Preço', ylabel_lower='Volume')
