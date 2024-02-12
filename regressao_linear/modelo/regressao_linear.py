import os
import pickle
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm

# Ler o dataset
dataset = pd.read_csv("C:\\TrabalhoMLOPS\\regressao_linear\\modelo\\bases\\loan_default_WITHOUT_NA.csv", sep=";", decimal=".")

# Dropar a coluna id
dataset.drop(columns=['ID'], inplace=True)

# Aplicar label encoding nas colunas de texto
for coluna in dataset.select_dtypes(include=['object']).columns:
    dataset[coluna] = pd.factorize(dataset[coluna])[0]

# Transformar todas as colunas para tipo número
dataset = dataset.apply(pd.to_numeric, errors='coerce')

# Remover linhas com valores faltantes
dataset.dropna(inplace=True)

# Features selecionadas
features_selecionadas = ["loan_limit", "Gender", "loan_type", "loan_purpose", "Credit_Worthiness", "open_credit", "income", "Status"]

# Dataset filtrado com as melhores features + Status
dataset_filtrado = dataset[features_selecionadas]

# Criação de bases de treino e teste
np.random.seed(123)
observacoes = len(dataset_filtrado)
t_treinamento = 0.8
t_teste = 0.2
t_treinamento = round(observacoes * t_treinamento)
t_teste = observacoes - t_treinamento
amostra = np.random.permutation(observacoes)

# Criação de bases de treino e teste
base_treino = dataset_filtrado.iloc[amostra[:t_treinamento]]
base_teste = dataset_filtrado.iloc[amostra[t_treinamento:]]

# Modelo de regressão linear
modelo_atual = sm.OLS(base_treino['Status'], sm.add_constant(base_treino.drop(columns=['Status']))).fit()

# Resumo do modelo
print(modelo_atual.rsquared)

# Previsão do modelo de regressão linear
predict_atual = modelo_atual.predict(sm.add_constant(base_teste.drop(columns=['Status'])))
erros_quadrados_rl_atual = (base_teste['Status'] - predict_atual) ** 2
rmse = np.sqrt(np.mean(erros_quadrados_rl_atual))
print(rmse)

# Criando matrizes para XGBoost
xgtrain = xgb.DMatrix(data=base_treino.drop(columns=['Status']), label=base_treino['Status'])
xgtest = xgb.DMatrix(data=base_teste.drop(columns=['Status']), label=base_teste['Status'])

# Parâmetros do modelo XGBoost
parametros = {'objective': 'reg:squarederror',
              'eta': 0.01,
              'min_child_weight': 3,
              'subsample': 0.8,
              'colsample_bytree': 0.8,
              'scale_pos_weight': 1.0,
              'gamma': 0,
              'max_depth': 8}

# Criando o modelo XGBoost
modelxg = xgb.train(params=parametros,
                    dtrain=xgtrain,
                    num_boost_round=5000,
                    evals=[(xgtrain, 'train'), (xgtest, 'val')],
                    early_stopping_rounds=10,
                    maximize=False)

# Predição do modelo XGBoost
values_predict = modelxg.predict(xgtest, iteration_range=(0, modelxg.best_iteration))

# RMSE
rmse = np.sqrt(mean_squared_error(base_teste['Status'], values_predict))
print(rmse)

# R²
r2 = 1 - sum((base_teste['Status'] - values_predict) ** 2) / sum((base_teste['Status'] - base_teste['Status'].mean()) ** 2)
print(r2)

# Teste de Resíduos
residuos = base_teste['Status'] - values_predict
residuos_dataf = pd.DataFrame({'values_predict': values_predict, 'residuals': residuos})

# Plot dos resíduos
sm.graphics.qqplot(residuos, line='45')

# Armazene o modelo, a acurácia e o R² em um dicionário
modelo_com_metricas = {
    'modelxg': modelxg,
    'rmse': rmse,
    'r2': r2
}

# Diretório da nova pasta
diretorio_app = '../app/'

# Verifica se o diretório existe, caso contrário, cria
if not os.path.exists(diretorio_app):
    os.makedirs(diretorio_app)

# Caminho completo para o arquivo pickle na nova pasta
caminho_pickle = os.path.join(diretorio_app, 'modelo_regressao_linear_xgboost.pkl')

# Salvar o modelo pickle na nova pasta
with open(caminho_pickle, 'wb') as file:
    pickle.dump(modelo_com_metricas, file)