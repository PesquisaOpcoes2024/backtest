import pandas as pd
import sqlite3

def create_db(csv_file, db_name, table_name):
    df = pd.read_csv(csv_file)

    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

    print(f"Dados do arquivo {csv_file} foram importados para a tabela '{table_name}' no banco de dados '{db_name}'")

# Parâmetros
csv_file = 'trade.csv'
db_name = 'metatrader.db'
table_name = 'trade'

# Criar o banco de dados e inserir os dados
create_db(csv_file, db_name, table_name)
