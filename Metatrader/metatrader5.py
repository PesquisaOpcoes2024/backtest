# é necessário rodar primeiro o comando 'pip install Metatrader5'
# é necessário rodar primeiro o comando 'pip install pip install pandas'
# é necessário rodar primeiro o comando 'pip install pip install ipykernel'
# é também necessário criar um arquivo de texto na pasta que possua 
# o login do MetaTrader5 na primeira linha e a senha na segunda
# %%
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import csv
import sqlite3

#Função para capturar os dados do MetaTrader 5 e salvar no arquivo csv

# def capture_data_to_csv(filename):
#     with open(filename, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real'])
        
#         with open('credentials.txt') as cred:
#             login, password = cred.read().split()
        
#         mt5.initialize(login=int(login), password=password, server='mt5.xpi.com.br:443')
#         #ticks
#         ticks = mt5.copy_ticks_range(
#             'PETR4',
#             datetime(2024, 5, 1),
#             datetime(2024, 6, 1), 
#             mt5.COPY_TICKS_TRADE
#         )
        
#         df_ticks = pd.DataFrame(ticks)
#         df_ticks["time"]=pd.to_datetime(df_ticks["time"], unit='s')
#         df_ticks["time_msc"]=pd.to_datetime(df_ticks["time"], unit='s')
        
#         for index, row in df_ticks.iterrows():
#             writer.writerow([
#                 row["time"],
#                 row["bid"],
#                 row["ask"],
#                 row["last"],
#                 row["volume"],
#                 row["time_msc"],
#                 row["flags"],
#                 row["volume_real"],
#             ])
             
#     print("Dados exportados para trade.csv")

def capture_data_to_csv(filename):
    try:
        with open('credentials.txt') as cred:
            login, password = cred.read().strip().split()

        print("Tentando inicializar o MetaTrader 5...")
        if not mt5.initialize(login=int(login), password=password, server='mt5.xpi.com.br:443'):
            print("Erro ao inicializar o MetaTrader 5:", mt5.last_error())
            return

        print("MetaTrader 5 inicializado com sucesso.")
        
        symbols = mt5.symbols_get()
        if symbols is None:
            print("Erro ao obter símbolos:", mt5.last_error())
            mt5.shutdown()
            return
        
        petr_symbols = [s.name for s in symbols if s.name.startswith('PETR4')]
        if not petr_symbols:
            print("Nenhum símbolo encontrado começando com 'PETR4'")
            mt5.shutdown()
            return
        
        print(f"Símbolos encontrados: {petr_symbols}")
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['symbol', 'time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags'])
            
            for symbol in petr_symbols:
                end_time = datetime.now()
                start_time = end_time - timedelta(days=7)  # Tentar um período menor de 7 dias
                
                print(f"Buscando ticks para {symbol} de {start_time} a {end_time}")
                
                ticks = mt5.copy_ticks_range(
                    symbol,
                    start_time,
                    end_time,
                    mt5.COPY_TICKS_TRADE
                )
                
                if ticks is None or len(ticks) == 0:
                    print(f"Erro ao copiar ticks para o símbolo {symbol} ou nenhum dado encontrado: {mt5.last_error()}")
                    continue
                
                df_ticks = pd.DataFrame(ticks)
                df_ticks["time"] = pd.to_datetime(df_ticks["time"], unit='s')
                df_ticks["time_msc"] = pd.to_datetime(df_ticks["time_msc"], unit='ms')
                df_ticks["symbol"] = symbol
                
                for index, row in df_ticks.iterrows():
                    writer.writerow([
                        row["symbol"],
                        row["time"],
                        row["bid"],
                        row["ask"],
                        row["last"],
                        row["volume"],
                        row["time_msc"],
                        row["flags"]
                    ])
                print(f"Dados exportados para o símbolo {symbol}")

        mt5.shutdown()
        print(f"Dados exportados para {filename}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
            

def add_csv_to_database(csv_file, db_file, table_name):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists='append', index=False) #if_exists='append' --> passar para replace
    conn.close()
    print(f"Dados do arquivo {csv_file} foram adicionados à tabela '{table_name}' no banco de dados '{db_file}'")

# Nome dos arquivos e tabela
csv_file = 'trade.csv'
db_file = 'metatrader.db'
table_name = 'trade'

# Capturar dados e salvar no arquivo CSV
capture_data_to_csv(csv_file)

# Adicionar os dados do CSV ao banco de dados SQLite
add_csv_to_database(csv_file, db_file, table_name)