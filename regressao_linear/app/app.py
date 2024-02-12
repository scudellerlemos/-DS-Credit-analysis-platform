import json
from flask import Flask, request, jsonify
import xgboost as xgb
import pickle
import pandas as pd

app = Flask(__name__)

# Carregar o modelo treinado
with open('modelo_regressao_linear_xgboost.pkl', 'rb') as file:
    model = pickle.load(file)

# Rota para inicial
@app.route('/', methods=['GET'])
def home():
    return 'Modelo de regressão linear para análise de propensão à inadimplencia.'

# Rota para fazer previsões
@app.route('/predict', methods=['POST'])
def predict():
    # Obter os dados da solicitação
    data = request.get_json(force=True)
    
    # Converter os dados em um DataFrame pandas
    df = pd.DataFrame(data)
    
    # Fazer previsões usando o modelo carregado
    predictions = model["modelxg"].predict(xgb.DMatrix(df))
    
    # Enviar as previsões de volta como resposta
    return jsonify({'predictions': predictions.tolist(), "r2": model["r2"], "rmse": model["rmse"]})    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
