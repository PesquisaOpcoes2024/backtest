# %%
import pandas as pd
import sqlite3

csv_file = 'trade.csv'
df = pd.read_csv(csv_file)

conn = sqlite3.connect('metatrader.db')
table_name = 'trade'
df.to_sql(table_name, conn, if_exists='replace', index=False)

conn.close()

print(f"Dados do arquivo {csv_file} foram importados para a tabela '{table_name}' no banco de dados 'bancos/seu_banco_de_dados.db'")