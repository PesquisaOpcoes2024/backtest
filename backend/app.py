from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return jsonify({'message': 'Conectado com sucesso!', 'data': [1, 2, 3, 4, 5]})

if __name__ == '__main__':
    app.run(port=5000)