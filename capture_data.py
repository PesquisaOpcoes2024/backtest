# %%
import sys

try:
    import yfinance as yf
    import pandas as pd
    import sqlite3
    from multiprocessing import Pool
    import csv
    print("Todas as bibliotecas foram importadas com sucesso.")
except ImportError as e:
    print(f"Erro ao importar bibliotecas: {e}")
    sys.exit(1)

def capture_data(symbol):
    try:
        print(f"Iniciando captura de dados para {symbol}...")
        df_ticks = yf.download(symbol, start="2024-04-01", end="2024-06-01", interval="1d")

        if df_ticks.empty:
            print(f"Nenhum dado encontrado para {symbol}")
            return None

        print(f"Dados capturados para {symbol}:\n{df_ticks.head()}")

        df_ticks["symbol"] = symbol
        df_ticks.reset_index(inplace=True)
        print(f"Dados processados para {symbol} com sucesso.")
        return df_ticks

    except Exception as e:
        print(f"Erro ao capturar dados para {symbol}: {e}")
        return None

def save_to_csv(dataframes, filename):
    try:
        print(f"Salvando dados no arquivo {filename}...")
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['symbol', 'Datetime', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
            for df in dataframes:
                if df is not None and not df.empty:
                    for index, row in df.iterrows():
                        writer.writerow([
                            row["symbol"],
                            row["Date"],
                            row["Open"],
                            row["High"],
                            row["Low"],
                            row["Close"],
                            row["Adj Close"],
                            row["Volume"]
                        ])
        print(f"Dados salvos no arquivo {filename} com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar dados no arquivo CSV: {e}")

def capture_all_options_to_csv(base_symbol, filename):
    print("Iniciando captura de dados de múltiplos símbolos...")
    petr_symbols = [base_symbol, 'PETR4.SA']

    try:
        with Pool() as pool:
            dataframes = pool.map(capture_data, petr_symbols)
        save_to_csv(dataframes, filename)
        print("Captura e salvamento de dados concluídos.")
    except Exception as e:
        print(f"Erro durante o processo de captura e salvamento: {e}")

def add_csv_to_database(csv_file, db_file, table_name):
    try:
        print(f"Iniciando a adição de dados do arquivo {csv_file} ao banco de dados {db_file}...")
        df = pd.read_csv(csv_file)
        print(f"Dados lidos do arquivo {csv_file}:\n{df.head()}")
        conn = sqlite3.connect(db_file)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        print(f"Dados do arquivo {csv_file} foram adicionados à tabela '{table_name}' no banco de dados '{db_file}' com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar dados ao banco de dados: {e}")

csv_file = 'trade.csv'
db_file = 'metatrader.db'
table_name = 'trade'

try:
    capture_all_options_to_csv('PETR4.SA', csv_file)
except Exception as e:
    print(f"Erro durante a captura e salvamento dos dados: {e}")

try:
    add_csv_to_database(csv_file, db_file, table_name)
except Exception as e:
    print(f"Erro ao adicionar os dados ao banco de dados: {e}")