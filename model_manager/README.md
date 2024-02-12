# Classe ModelManagerApp

A classe ModelManagerApp gerencia modelos de aprendizado de máquina para previsão de empréstimos.

## Atributos

- **API_REGRESSAO_LINEAR_URL (str)**: URL para o endpoint da API do modelo de regressão.
- **API_CLUSTERIZACAO_URL (str)**: URL para o endpoint da API do modelo de clusterização.
- **API_CLASSIFICACAO_URL (str)**: URL para o endpoint da API do modelo de classificação.
- **MODEL_MANAGER_URL (str)**: URL para o Model Manager.

## Métodos

### Método `__init__(api_regressao_linear_url, api_clusterizacao_url, api_classificacao_url, model_manager_url)`

Inicializa a classe ModelManagerApp com URLs das APIs.

### Método `home()`

Renderiza a página inicial da aplicação.

### Método `submit(request_form)`

Manipula o envio do formulário e prevê a aprovação do empréstimo.

### Método `dashboard_regressao_linear()`

Renderiza o painel para monitoramento de desvio de dados do modelo de regressão.

### Método `dashboard_clusterizacao()`

Renderiza o painel para monitoramento de desvio de dados do modelo de clusterização.

### Método `dashboard_classificacao()`

Renderiza o painel para monitoramento de desvio de dados do modelo de classificação.

### Método `regressao_linear(dados, uuid_valor)`

Prevê a aprovação do empréstimo usando o modelo de regressão.

### Método `clusterizacao(dados, uuid_valor)`

Prevê o cluster de aprovação de empréstimo usando o modelo de clusterização.

### Método `classificacao(dados, uuid_valor)`

Prevê a classe de aprovação de empréstimo usando o modelo de classificação.

### Método `json_regressao_linear(dados)`

Converte os dados de entrada para o formato JSON para a previsão do modelo de regressão.

### Método `json_clusterizacao_classificacao(dados)`

Converte os dados de entrada para o formato JSON para a previsão dos modelos de clusterização e classificação.

### Método `json_data_drift_regressao_linear(dados)`

Formata as estatísticas de desvio de dados do modelo de regressão para exibição.

### Método `aprovar_emprestimo(uuid_valor, aprovado)`

Aprova ou rejeita um empréstimo com base na entrada do usuário.

