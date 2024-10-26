import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data_from_db(db_file):
    # Conecta ao banco de dados
    conn = sqlite3.connect(db_file)

    # Consulta os dados necessários
    query = """
    SELECT due_date, open, close FROM opcoes
    WHERE symbol = 'PETR4'
    ORDER BY due_date
    """
    df = pd.read_sql_query(query, conn)

    # Fecha a conexão com o banco de dados
    conn.close()
    return df

def plot_price_vs_time(df):
    # Converte a coluna due_date para datetime
    df['due_date'] = pd.to_datetime(df['due_date'])
    
    # Plota o gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(df['due_date'], df['open'], label='Abertura', marker='o')
    plt.plot(df['due_date'], df['close'], label='Fechamento', marker='x')
    plt.title('Preço x Tempo do Ativo PETR4')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('preco_x_tempo_petr4.png')  # Salva a imagem do gráfico
    plt.show()  # Mostra o gráfico

def main():
    db_file = 'meu_banco_de_dados.db'  # Nome do arquivo do banco de dados
    df = fetch_data_from_db(db_file)
    
    if not df.empty:
        plot_price_vs_time(df)
    else:
        print("Nenhum dado encontrado para o ativo PETR4.")

if __name__ == "__main__":
    main()
