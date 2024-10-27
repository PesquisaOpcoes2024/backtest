from flask import Flask, jsonify, request
from datetime import datetime
import pandas as pd
import sqlite3
import requests
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Função para buscar dados da API
def fetch_options_data(symbol, access_token, resolution, from_date, to_date):
    url = f'https://api.oplab.com.br/v3/market/historical/{symbol}/{resolution}?from={from_date}&to={to_date}&raw=false&smooth=false&df=true'
    headers = {'Access-Token': access_token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Função para calcular o RSI
def calculate_rsi(data, column, window=14):
    data = data.copy()
    
    # Calcula ganhos e perdas diários
    data['Variation'] = data[column].diff()
    data['Gain'] = np.where(data['Variation'] > 0, data['Variation'], 0)
    data['Loss'] = np.where(data['Variation'] < 0, -data['Variation'], 0)

    # Calcula médias móveis exponenciais de ganho e perda
    avg_gain = data['Gain'].rolling(window=window).mean()
    avg_loss = data['Loss'].rolling(window=window).mean()
    
    # Calcula o RS e o RSI
    RS = avg_gain / avg_loss.replace(0, np.nan)  # Evita divisão por zero
    RSI = 100 - (100 / (1 + RS))
    
    return RSI

# Endpoint para obter dados do gráfico
@app.route('/api/data', methods=['GET'])
def get_data():
    symbol = request.args.get('symbol')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    resolution = "1d"
    access_token = 'qUoxkqtK2dhIa4q3Ir9yqwnuYMvfYnHLtedgxM/EjBZHqE7SQv8/0ZE7y+nukIYZ--XhgBD6EPwF8T0Ffj4y3u1A==--ZTNjNDZiMDNkZGQ0MzBlMjFhMGQ4OGVhN2MyMWVkMzE='

    options_data = fetch_options_data(symbol, access_token, resolution, from_date, to_date)
    if options_data and 'data' in options_data:
        data = pd.DataFrame(options_data['data'])

        data['date'] = pd.to_datetime(data['time'], unit='ms')

        monthly_data = data.resample('MS', on='date').agg({
            'close': 'last',
            'high': 'max',
            'low': 'min',
            'open': 'first',
            'volume': 'sum'
        }).reset_index()

        formatted_data = monthly_data.round(2).to_dict(orient='records')
        return jsonify(formatted_data), 200

    return jsonify({'error': 'Dados não encontrados'}), 404

@app.route('/api/ifr', methods=['GET'])
def get_ifr():
    symbol = request.args.get('symbol')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    resolution = "1d"
    access_token = 'qUoxkqtK2dhIa4q3Ir9yqwnuYMvfYnHLtedgxM/EjBZHqE7SQv8/0ZE7y+nukIYZ--XhgBD6EPwF8T0Ffj4y3u1A==--ZTNjNDZiMDNkZGQ0MzBlMjFhMGQ4OGVhN2MyMWVkMzE='

    
    print(f"Fetching data for symbol: {symbol}, from: {from_date}, to: {to_date}")

    options_data = fetch_options_data(symbol, access_token, resolution, from_date, to_date)
    if options_data and 'data' in options_data:
        data = pd.DataFrame(options_data['data'])
        data['date'] = pd.to_datetime(data['time'], unit='ms')

        # Calcular o RSI
        rsi_values = calculate_rsi(data, 'close')

        # Adiciona o RSI ao DataFrame
        data['RSI'] = rsi_values

        # Seleciona apenas as colunas relevantes para o frontend
        rsi_data = data[['date', 'RSI']].dropna()

        formatted_data = rsi_data.round(2).to_dict(orient='records')
        return jsonify(formatted_data), 200

    print("No data found or invalid response.")
    return jsonify({'error': 'Dados não encontrados'}), 404


if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/api/ifr', methods=['GET'])
# def get_ifr():