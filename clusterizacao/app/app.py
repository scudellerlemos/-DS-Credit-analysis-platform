import json
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Carregar o modelo treinado
model = joblib.load('cluster_knn_metricas.pkl')

# Rota para inicial
@app.route('/', methods=['GET'])
def home():
    return 'Modelo de clusterizacao KNN para análise de propensão à inadimplencia.'

# Rota para fazer previsões
@app.route('/predict', methods=['POST'])
def predict():
    # Obter os dados da solicitação
    data = request.get_json(force=True)
    
    # Converter os dados em um DataFrame pandas
    df = pd.DataFrame(data)
    
    # Fazer previsões usando o modelo carregado
    predictions = model["cluster"].predict(df)
    
    # Enviar as previsões de volta como resposta
    return jsonify({'predictions': predictions.tolist(), "r2": model["r2"], "rmse": model["rmse"]})   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
