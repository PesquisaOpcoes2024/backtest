from flask import Flask, jsonify, request
from datetime import datetime
import pandas as pd
import sqlite3
import requests
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/api/ifr', methods=['GET'])
# def get_ifr():