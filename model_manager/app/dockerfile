# Use a imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o código da aplicação para o contêiner
COPY . .

# Instala as dependências especificadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000
EXPOSE 5000

# Comando de inicialização
CMD ["python", "app.py"]