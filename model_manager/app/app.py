from datetime import date
import json
import os
import uuid
from flask import Flask, render_template, request, jsonify
import requests
import xgboost as xgb
import pickle
import pandas as pd
import database as db

API_REGRESSAO_LINEAR_URL = os.environ["API_REGRESSAO_LINEAR_URL"]
API_CLUSTERIZACAO_URL = os.environ["API_CLUSTERIZACAO_URL"]
API_CLASSIFICACAO_URL = os.environ["API_CLASSIFICACAO_URL"]
MODEL_MANAGER_URL = os.environ["MODEL_MANAGER_URL"]

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Rota para inicial
@app.route('/', methods=['GET'])
def home():
    return render_template('formulario.html', valor_predito=0, MODEL_MANAGER_URL=MODEL_MANAGER_URL)

@app.route('/submit', methods=['POST'])
def submit():
    action = request.form['action']  # Obtém o valor do atributo 'name' do botão clicado

    if action == 'Enviar':
        uuid_valor = uuid.uuid4()
        
        dados = request.form
        nome = request.form['nome']
        income = request.form['income']
        loan_limit = request.form['loan_limit']
        Gender = request.form['Gender']
        loan_type = request.form['loan_type']
        loan_purpose = request.form['loan_purpose']
        Credit_Worthiness = request.form['Credit_Worthiness']
        open_credit = request.form['open_credit']

        valor_predito = regressao_linear(dados, uuid_valor)    
        cluster = clusterizacao(dados, uuid_valor)    
        classificado = classificacao(dados, uuid_valor) 

        if classificado == 1:
            classificado = 'EQUI'
        elif classificado == 2:
            classificado = 'CRIF'
        elif classificado == 3:
            classificado = 'CIB'
        else:
            classificado = 'EXP'

        return render_template('formulario.html', cluster=cluster,classificado=classificado,MODEL_MANAGER_URL=MODEL_MANAGER_URL, uuid_valor=uuid_valor, nome=nome, income=income, loan_limit=loan_limit, Gender=Gender, loan_type=loan_type, loan_purpose=loan_purpose, Credit_Worthiness=Credit_Worthiness, open_credit=open_credit, valor_predito=round(valor_predito * 100, 2), classe="verde" if valor_predito < 0.2 else "vermelho")
    elif action == 'Aprovar':        
        emprestimo_aprovado = 1
    else:
        emprestimo_aprovado = 0

    uuid_valor = request.form['uuid_valor']
    aprovar_emprestimo(uuid_valor=uuid_valor, aprovado=emprestimo_aprovado)        
    return render_template('aprovacao.html', emprestimo_aprovado=emprestimo_aprovado)

# Rota para dashboard_regressao_linear
@app.route('/dashboard_regressao_linear', methods=['GET'])
def dashboard_regressao_linear():
    json_formatado = json_data_drift_regressao_linear(db.busca_dados_data_drift('regressao_linear'))
    print(json_formatado)

    return render_template('dashboard_regressao_linear.html', MODEL_MANAGER_URL=MODEL_MANAGER_URL, json_formatado=json_formatado)

# Rota para dashboard_clusterizacao
@app.route('/dashboard_clusterizacao', methods=['GET'])
def dashboard_clusterizacao():
    json_formatado = json_data_drift_regressao_linear(db.busca_dados_data_drift('clusterizacao_knn'))

    return render_template('dashboard_clusterizacao.html', MODEL_MANAGER_URL=MODEL_MANAGER_URL, json_formatado=json_formatado)

# Rota para dashboard_classificacao
@app.route('/dashboard_classificacao', methods=['GET'])
def dashboard_classificacao():
    json_formatado = json_data_drift_regressao_linear(db.busca_dados_data_drift('classificacao'))

    return render_template('dashboard_classificacao.html', MODEL_MANAGER_URL=MODEL_MANAGER_URL, json_formatado=json_formatado)

def regressao_linear(dados, uuid_valor):
    url = f"{API_REGRESSAO_LINEAR_URL}/predict"
    json_montado = json_regressao_linear(dados)    
    
    response = requests.post(url, json.dumps(json_montado))

    valor_predito = eval(response.content.decode('utf-8'))["predictions"][0]    
    r2 = eval(response.content.decode('utf-8'))["r2"]
    rmse = eval(response.content.decode('utf-8'))["rmse"]    
    
    retorno, status = db.grava_log(uuid_valor, date.today(), "regressao_linear", dados['nome'], dados['loan_limit'], dados['Gender'], dados['loan_type'], dados['loan_purpose'], dados['Credit_Worthiness'], dados['open_credit'], dados['income'], valor_predito, r2, rmse)

    return valor_predito

def clusterizacao(dados, uuid_valor):
    url = f"{API_CLUSTERIZACAO_URL}/predict"
    json_montado = json_clusterizacao_classificacao(dados)    
    
    response = requests.post(url, json.dumps(json_montado))

    valor_predito = eval(response.content.decode('utf-8'))["predictions"][0]    
    r2 = eval(response.content.decode('utf-8'))["r2"]
    rmse = eval(response.content.decode('utf-8'))["rmse"]    
    
    retorno, status = db.grava_log(uuid_valor, date.today(), "clusterizacao_knn", dados['nome'], dados['loan_limit'], dados['Gender'], dados['loan_type'], dados['loan_purpose'], dados['Credit_Worthiness'], dados['open_credit'], dados['income'], valor_predito, r2, rmse)
 
    return valor_predito

def classificacao(dados, uuid_valor):
    url = f"{API_CLASSIFICACAO_URL}/predict"
    json_montado = json_clusterizacao_classificacao(dados)    
    
    response = requests.post(url, json.dumps(json_montado))

    valor_predito = eval(response.content.decode('utf-8'))["predictions"][0]    
    r2 = eval(response.content.decode('utf-8'))["r2"]
    rmse = eval(response.content.decode('utf-8'))["rmse"]    
    
    retorno, status = db.grava_log(uuid_valor, date.today(), "classificacao", dados['nome'], dados['loan_limit'], dados['Gender'], dados['loan_type'], dados['loan_purpose'], dados['Credit_Worthiness'], dados['open_credit'], dados['income'], valor_predito, r2, rmse)
 
    return valor_predito
    
def json_regressao_linear(dados):
    # Converter os dados para o formato JSON desejado
    dados_json = [
        {
            "loan_limit": int(dados['loan_limit']),
            "Gender": int(dados['Gender']),
            "loan_type": int(dados['loan_type']),
            "loan_purpose": int(dados['loan_purpose']),
            "Credit_Worthiness": int(dados['Credit_Worthiness']),
            "open_credit": int(dados['open_credit']),
            "income": float(dados['income'])
        }
    ]
    
    # Retornar os dados em formato JSON 
    return dados_json

def json_clusterizacao_classificacao(dados):
    # Converter os dados para o formato JSON desejado
    dados_json = [
        {
            "open_credit": int(dados['open_credit']),
            "Credit_Worthiness": int(dados['Credit_Worthiness']),
            "loan_purpose": int(dados['loan_purpose']),
            "Gender": int(dados['Gender']),
            "loan_type": int(dados['loan_type']),
            "loan_limit": int(dados['loan_limit']),
            "income": float(dados['income'])
        }
    ]
    
    # Retornar os dados em formato JSON 
    return dados_json

def json_data_drift_regressao_linear(dados):
   # Extrair os dados da primeira parte da tupla
    dados, status = dados

    # Lista para armazenar os dados formatados
    dados_formatados = []

    # Iterar sobre os dados e formatá-los
    print(dados[0])
    for linha in dados:
        linha_formatada = {
            'uuid_valor': linha[1],
            'data_cotacao': linha[2].isoformat(),  # Convertendo o objeto date para string no formato ISO
            'metodo': linha[3],
            'nome_cliente': linha[4],
            'loan_limit': linha[5],
            'gender': linha[6],
            'loan_type': linha[7],
            'loan_purpose': linha[8],
            'credit_worthiness': linha[9],
            'open_credit': linha[10],
            'income': float(linha[11]),  # Convertendo Decimal para float
            'valor_predito': float(linha[12]),  # Convertendo Decimal para float
            'r2': float(linha[13]),  # Convertendo Decimal para float
            'rmse': float(linha[14]),  # Convertendo Decimal para float
            'emprestimo_aprovado': linha[15]
        }
        dados_formatados.append(linha_formatada)

    # Convertendo os dados formatados para JSON
    return json.dumps(dados_formatados)

def aprovar_emprestimo(uuid_valor, aprovado):
    uuid_valor = db.aprovar_emprestimo(uuid_valor=uuid_valor, aprovado=aprovado)    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
