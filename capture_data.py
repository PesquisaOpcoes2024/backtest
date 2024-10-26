import requests
import pandas as pd

def fetch_historical_options_data(symbol, access_token, start_date, end_date):
    """Faz a requisição à API para obter dados históricos das opções."""
    url = f"https://api.oplab.com.br/v3/historical/options/{symbol}"
    headers = {
        'Access-Token': access_token
    }
    
    # Parâmetros para a data inicial e final
    params = {
        'start_date': start_date,  # Formato 'YYYY-MM-DD'
        'end_date': end_date       # Formato 'YYYY-MM-DD'
    }

    # Faz a requisição GET
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()  # Retorna os dados JSON
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return None

def process_historical_data(data):
    """Processa os dados históricos e os organiza em uma lista de dicionários."""
    if data is None:
        print("Nenhum dado para processar.")
        return []

    historical_data = []
    for entry in data:
        historical_data.append({
            'date': entry.get('date'),
            'open': entry.get('open'),
            'high': entry.get('high'),
            'low': entry.get('low'),
            'close': entry.get('close'),
            'volume': entry.get('volume'),
            'adjusted_close': entry.get('adjusted_close'),
        })
    return historical_data

def save_to_csv(data, filename):
    """Salva os dados em um arquivo CSV."""
    if not data:
        print("Nenhum dado disponível para salvar.")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Dados salvos em {filename}")

def main():
    symbol = "PETR4"
    access_token = "qUoxkqtK2dhIa4q3Ir9yqwnuYMvfYnHLtedgxM/EjBZHqE7SQv8/0ZE7y+nukIYZ--XhgBD6EPwF8T0Ffj4y3u1A==--ZTNjNDZiMDNkZGQ0MzBlMjFhMGQ4OGVhN2MyMWVkMzE="
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    # Faz a requisição para obter os dados históricos
    data = fetch_historical_options_data(symbol, access_token, start_date, end_date)

    if data is not None:  # Verifica se dados foram retornados
        # Processa os dados
        processed_data = process_historical_data(data)
        # Salva os dados em um arquivo CSV
        save_to_csv(processed_data, 'historical_options_data.csv')
    else:
        print(f"Nenhum dado retornado para o símbolo {symbol}.")

if __name__ == "__main__":
    main()
