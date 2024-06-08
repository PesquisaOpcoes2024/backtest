# é necessário rodar primeiro o comando 'pip install Metatrader5'
# é também necessário criar um arquivo de texto na pasta que possua 
# o login do MetaTrader5 na primeira linha e a senha na segunda
# %%
import MetaTrader5 as mt5
from datetime import datetime, time
import pandas as pd
import csv
import sqlite3
import schedule

#Função para capturar os dados do MetaTrader 5 e salvar no arquivo csv
def capture_data_to_csv(filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real'])
        
        with open('credentials.txt') as cred:
            login, password = cred.read().split()
        
        mt5.initialize(login=int(login), password=password, server='mt5.xpi.com.br:443')
        #ticks
        ticks = mt5.copy_ticks_range(
            'PETR4',
            datetime(2024, 5, 1),
            datetime(2024, 6, 1), 
            #extremamente importante se atentar a essas datas selecionadas
            mt5.COPY_TICKS_TRADE
        )
        
        df_ticks = pd.DataFrame(ticks)
        df_ticks["time"]=pd.to_datetime(df_ticks["time"], unit='s')
        df_ticks["time_msc"]=pd.to_datetime(df_ticks["time"], unit='s')
        
        for index, row in df_ticks.iterrows():
            writer.writerow([
                row["time"],
                row["bid"],
                row["ask"],
                row["last"],
                row["volume"],
                row["time_msc"],
                row["flags"],
                row["volume_real"],
            ])
             
    print("Dados exportados para trade.csv")
            

#Função para ler os dados do arquivo CSV e adicioná-los ao banco de dados SQLite
def add_csv_to_database(csv_file, db_file, table_name):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
    print(f"Dados do arquivo {csv_file} foram adicionados à tabela '{table_name}' no banco de dados '{db_file}'")

# Nome dos arquivos e tabela
csv_file = 'trade.csv'
db_file = 'metatrader.db'
table_name = 'trade'

# Agendar a execução da captura de dados e adição ao banco de dados
schedule.every().day.at("23:59").do(capture_data_to_csv, csv_file)
schedule.every().day.at("00:00").do(add_csv_to_database, csv_file, db_file, table_name)

# Loop infinito para executar o agendador
while True:
    schedule.run_pending()
    time.sleep(60) # Espera 1 minuto antes de verificar novamente se há tarefas agendadas