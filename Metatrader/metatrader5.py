# é necessário rodar primeiro o comando 'pip install Metatrader5'
# é necessário rodar primeiro o comando 'pip install pip install pandas'
# é necessário rodar primeiro o comando 'pip install pip install ipykernel'
# é também necessário criar um arquivo de texto na pasta que possua 
# o login do MetaTrader5 na primeira linha e a senha na segunda
# %%
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import csv
import sqlite3
from multiprocessing import Pool

#Função para capturar os dados do MetaTrader 5 e salvar no arquivo csv
def initialize_mt5():
    with open('credentials.txt') as cred:
        login, password = cred.read().split()
    if not mt5.initialize(login=int(login), password=password, server='mt5.xpi.com.br:443'):
        print("Falha ao inicializar MetaTrader 5")
        return False
    return True

def shutdown_mt5():
    mt5.shutdown()

def capture_data(symbol):
    try:
        if not mt5.symbol_info(symbol):
            return None
        
        ticks = mt5.copy_ticks_range(
            symbol,
            datetime(2024, 5, 1),
            datetime(2024, 6, 1), 
            mt5.COPY_TICKS_TRADE
        )
        
        if len(ticks) == 0:
            return None

        df_ticks = pd.DataFrame(ticks)
        df_ticks["symbol"] = symbol
        df_ticks["time"] = pd.to_datetime(df_ticks["time"], unit='s')
        df_ticks["time_msc"] = pd.to_datetime(df_ticks["time_msc"], unit='ms')
        
        return df_ticks

    except Exception as e:
        print(f"Erro ao capturar dados para {symbol}: {e}")
        return None

def save_to_csv(dataframes, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['symbol', 'time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real'])
        for df in dataframes:
            if df is not None:
                for index, row in df.iterrows():
                    writer.writerow([
                        row["symbol"],
                        row["time"],
                        row["bid"],
                        row["ask"],
                        row["last"],
                        row["volume"],
                        row["time_msc"],
                        row["flags"],
                        row["volume_real"],
                    ])

def capture_all_options_to_csv(base_symbol, filename):
    if not initialize_mt5():
        return

    all_symbols = mt5.symbols_get()
    petr_symbols = [symbol.name for symbol in all_symbols if symbol.name.startswith(base_symbol)]
    
    with Pool() as pool:
        dataframes = pool.map(capture_data, petr_symbols)
    
    save_to_csv(dataframes, filename)
    shutdown_mt5()

def add_csv_to_database(csv_file, db_file, table_name):
    try:
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(db_file)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        print(f"Dados do arquivo {csv_file} foram adicionados à tabela '{table_name}' no banco de dados '{db_file}'")
    except Exception as e:
        print("Erro ao adicionar dados ao banco de dados:", e)

# Nome dos arquivos e tabela
csv_file = 'trade.csv'
db_file = 'metatrader.db'
table_name = 'trade'

# Capturar dados e salvar no arquivo CSV
capture_all_options_to_csv('PETR', csv_file)

# Adicionar os dados do CSV ao banco de dados SQLite
add_csv_to_database(csv_file, db_file, table_name)


# %%

# %%

# %%
