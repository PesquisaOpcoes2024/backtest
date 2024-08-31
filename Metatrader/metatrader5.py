# %%
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import csv
import sqlite3

def capture_data_to_csv(filename):
    try:
        # Leitura das credenciais
        with open('credentials.txt') as cred:
            login, password = cred.read().strip().split()

        print("Tentando inicializar o MetaTrader 5...")
        if not mt5.initialize(login=int(login), password=password, server='mt5.xpi.com.br:443'):
            print("Erro ao inicializar o MetaTrader 5:", mt5.last_error())
            return

        print("MetaTrader 5 inicializado com sucesso.")

        symbol = 'PETR4'  # Foco apenas no ativo PETR4
        print(f"Buscando dados para o símbolo {symbol}...")

        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)  # Período de 7 dias

        # Coletando dados de ticks
        print(f"Buscando ticks para {symbol} de {start_time} a {end_time}")
        ticks = mt5.copy_ticks_range(symbol, start_time, end_time, mt5.COPY_TICKS_TRADE)

        if ticks is None or len(ticks) == 0:
            print(f"Erro ao copiar ticks para o símbolo {symbol} ou nenhum dado encontrado: {mt5.last_error()}")
            mt5.shutdown()
            return

        df_ticks = pd.DataFrame(ticks)
        df_ticks["time"] = pd.to_datetime(df_ticks["time"], unit='s')
        df_ticks["time_msc"] = pd.to_datetime(df_ticks["time_msc"], unit='ms')
        df_ticks["symbol"] = symbol

        # Coletando dados históricos
        print(f"Buscando dados históricos para {symbol} de {start_time} a {end_time}")
        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_D1, start_time, end_time)
        
        if rates is None or len(rates) == 0:
            print(f"Erro ao copiar dados históricos para o símbolo {symbol} ou nenhum dado encontrado: {mt5.last_error()}")
            mt5.shutdown()
            return
        
        df_rates = pd.DataFrame(rates)
        df_rates["time"] = pd.to_datetime(df_rates["time"], unit='s')

        # Salvando dados em CSV
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['symbol', 'time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'open', 'high', 'low', 'close'])
            
            for index, row in df_ticks.iterrows():
                # Encontrar a data correspondente no dataframe de dados históricos
                date_match = df_rates[df_rates["time"].dt.date == row["time"].date()]

                # Valores padrão como None, caso não haja correspondência
                open_val = date_match["open"].values[0] if not date_match.empty else None
                high_val = date_match["high"].values[0] if not date_match.empty else None
                low_val = date_match["low"].values[0] if not date_match.empty else None
                close_val = date_match["close"].values[0] if not date_match.empty else None

                writer.writerow([
                    row["symbol"],
                    row["time"],
                    row["bid"],
                    row["ask"],
                    row["last"],
                    row["volume"],
                    row["time_msc"],
                    row["flags"],
                    open_val,
                    high_val,
                    low_val,
                    close_val
                ])
            print(f"Dados exportados para o símbolo {symbol}")

        mt5.shutdown()
        print(f"Dados exportados para {filename}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def add_csv_to_database(csv_file, db_file, table_name):
    try:
        df = pd.read_csv(csv_file)
        conn = sqlite3.connect(db_file)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Dados do arquivo {csv_file} foram adicionados à tabela '{table_name}' no banco de dados '{db_file}'")
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar os dados ao banco de dados: {e}")

# Parâmetros
csv_file = 'trade.csv'
db_file = 'metatrader.db'
table_name = 'trade'

capture_data_to_csv(csv_file)
add_csv_to_database(csv_file, db_file, table_name)
# %%

# %%

# %%
