#%%
import requests
from datetime import datetime
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Função para buscar dados da API
def fetch_options_data(symbol, access_token, resolution, from_date, to_date):
    url = f'https://api.oplab.com.br/v3/market/historical/{symbol}/{resolution}?from={from_date}&to={to_date}&raw=false&smooth=false&df=true'
    headers = {'Access-Token': access_token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Retorna os dados JSON
    elif response.status_code == 204:
        print(f"Status code 204: No content for symbol {symbol}.")
        return None
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return None

# Função para formatar a data nos dados
def format_time_in_data(data_dict, time_field='time', output_format="%d/%m/%Y"):
    if 'data' in data_dict:
        for item in data_dict['data']:
            if time_field in item:
                timestamp = item[time_field] / 1000
                date_obj = datetime.fromtimestamp(timestamp)
                item['formatted_date'] = date_obj.strftime(output_format)
    return data_dict  # Retorna o dicionário atualizado

# Função para salvar dados em um CSV
def save_data_to_csv(data_dict, symbol, filename='options_data.csv'):
    if 'data' in data_dict:
        for item in data_dict['data']:
            item['symbol'] = symbol
            
        df = pd.DataFrame(data_dict['data'])
        
        # Arredondando os valores numéricos
        df['open'] = df['open'].round(2)
        df['high'] = df['high'].round(2)
        df['low'] = df['low'].round(2)
        df['close'] = df['close'].round(2)
        df['volume'] = df['volume'].round(0)
        df['fvolume'] = df['fvolume'].round(2)

        # Selecionando colunas
        df = df[['symbol', 'open', 'low', 'high', 'close', 'volume', 'fvolume', 'formatted_date']]
        
        df.to_csv(filename, index=False)
        print(f"Dados salvos em {filename} com sucesso.")

# Função para salvar dados em um banco de dados SQLite
def save_data_to_database(data_dict, symbol, db_name='options_data.db'):
    if 'data' in data_dict:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS options_data (
                symbol TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                fvolume REAL,
                formatted_date TEXT
            )
        ''')
        
        for item in data_dict['data']:
            cursor.execute('''
                INSERT INTO options_data (symbol, open, high, low, close, volume, fvolume, formatted_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (symbol, round(item['open'], 2), round(item['high'], 2), round(item['low'], 2), 
                  round(item['close'], 2), item['volume'], round(item['fvolume'], 2), item['formatted_date']))
        
        conn.commit()
        conn.close()
        print(f"Dados salvos no banco de dados {db_name} com sucesso.")

# Função para plotar gráfico Preço do Ativo x Tempo
# Função para plotar gráfico Preço do Ativo x Tempo
def plot_price_vs_time(symbol, db_name='options_data.db'):
    conn = sqlite3.connect(db_name)
    
    # Lê os dados do banco de dados
    query = f"SELECT formatted_date, close FROM options_data WHERE symbol='{symbol}' ORDER BY formatted_date"
    df = pd.read_sql(query, conn)
    
    conn.close()

    # Convertendo 'formatted_date' para datetime
    df['formatted_date'] = pd.to_datetime(df['formatted_date'], format="%d/%m/%Y")

    # Agrupar por data e calcular a média do preço de fechamento para evitar duplicados
    df = df.groupby('formatted_date', as_index=False).close.mean()

    # Verificando se há dados suficientes para plotar
    if df.empty:
        print(f"Nenhum dado encontrado para o símbolo {symbol}.")
        return

    # Configurando o gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(df['formatted_date'], df['close'], color='b', linewidth=1.5, label='Preço de Fechamento')
    
    # Personalizando o gráfico
    plt.title(f'Preço do Ativo {symbol} ao Longo do Tempo', fontsize=16)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Preço de Fechamento (R$)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.legend()
    plt.show()


def main():
    symbol = "PETR4"
    resolution = "1d"  
    from_date = "2000-01-01"
    to_date = "2024-01-01"
    access_token = 'qUoxkqtK2dhIa4q3Ir9yqwnuYMvfYnHLtedgxM/EjBZHqE7SQv8/0ZE7y+nukIYZ--XhgBD6EPwF8T0Ffj4y3u1A==--ZTNjNDZiMDNkZGQ0MzBlMjFhMGQ4OGVhN2MyMWVkMzE='

    options_data = fetch_options_data(symbol, access_token, resolution, from_date, to_date)

    if options_data is not None:
        formatted_data_dict = format_time_in_data(options_data)
        save_data_to_csv(formatted_data_dict, symbol)
        save_data_to_database(formatted_data_dict, symbol)
        plot_price_vs_time(symbol)
    else:
        print("Nenhum dado retornado da API.")

if __name__ == "__main__":
    main()
# %%
