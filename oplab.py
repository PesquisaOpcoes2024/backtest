import requests
import pandas as pd
import sqlite3
import re
import mplfinance as mpl
import matplotlib.dates as mdates  # Adicionar para formatação de data

# Faz a requisição à API e retorna os dados das opções
def fetch_options_data(symbol, access_token):
    url = f"https://api.oplab.com.br/v3/market/options/{symbol}"
    
    headers = {
        'Access-Token': access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Retorna os dados JSON
    elif response.status_code == 204:
        print(f"Status code 204: No content for symbol {symbol}.")
        print(f"Response headers: {response.headers}")
        return None
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return None

# Processa os dados e os organiza em uma lista de dicionários com as colunas necessárias
def process_options_data(data):
    options_data = []
    
    if data:
        for option in data:
            try:
                options_data.append({
                    'symbol': option.get('symbol'),
                    'name': option.get('name'),
                    'open': option.get('open'),
                    'high': option.get('high'),
                    'low': option.get('low'),
                    'close': option.get('close'),
                    'volume': option.get('volume'),
                    'strike': option.get('strike'),
                    'category': option.get('category'),
                    'exchange_id': option.get('exchange_id'),
                })
            except KeyError as e:
                print(f"Erro ao processar dados: Campo {e} não encontrado.")
    return options_data

# Salva os dados em um arquivo CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Dados salvos em {filename}")

# Adiciona os dados de um arquivo CSV a um banco de dados SQLite
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

# Função para extrair a data de vencimento do nome da opção
def extract_expiration_date(option_name):
    # Ajuste a regex conforme o formato das datas nos nomes das opções
    match = re.search(r'(\d{2}-\d{2}-\d{4})', option_name)
    if match:
        return pd.to_datetime(match.group(1), format='%d-%m-%Y', errors='coerce')
    return None

# Função para carregar dados do banco de dados SQLite e preparar o DataFrame
def load_data_from_database(db_file, table_name):
    try:
        conn = sqlite3.connect(db_file)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        print(f"Dados carregados da tabela '{table_name}' do banco de dados '{db_file}':\n{df.head()}")
        return df
    except Exception as e:
        print(f"Erro ao carregar dados do banco de dados: {e}")
        return pd.DataFrame()

# Função para plotar usando mplfinance (sem volume) e exibindo Mes/Ano no eixo
def plot_candlestick_with_mplfinance(df):
    # Remover linhas onde dados essenciais estão faltando
    df = df.dropna(subset=['open', 'high', 'low', 'close'])

    # Extrai a data de vencimento do campo 'name' e define como 'Date'
    df['Date'] = df['name'].apply(extract_expiration_date)

    # Remover linhas onde a data não foi extraída corretamente
    df = df.dropna(subset=['Date'])

    # Configura a coluna 'Date' como índice do DataFrame
    df.set_index('Date', inplace=True)

    # Manter apenas as colunas necessárias para o gráfico
    df = df[['open', 'high', 'low', 'close']]

    # Converte o índice 'Date' para o tipo datetime se já não estiver
    df.index = pd.to_datetime(df.index)

    # Plotar o gráfico de candlestick
    fig, axes = mpl.plot(df, type='candle', style='charles', title='Gráfico de Candlestick', ylabel='Preço', returnfig=True)

    # Configuração para mostrar apenas Mês/Ano no eixo de tempo
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  # Configura o formato para Mes/Ano
    fig.autofmt_xdate()  # Ajusta as datas para melhor visualização

    # Exibe o gráfico
    mpl.show()

# Função principal
def main():
    db_file = 'options_database.db'
    table_name = 'options'
    
    # Carregar os dados do banco de dados SQLite
    df = load_data_from_database(db_file, table_name)
    
    if not df.empty:
        # Plotar gráfico de candlestick usando mplfinance
        plot_candlestick_with_mplfinance(df)
    else:
        print("Nenhum dado encontrado no banco de dados para plotagem.")

if __name__ == "__main__":
    main()
