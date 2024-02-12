import psycopg2
from faker import Faker
import random
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

dbname = os.environ["dbname"]
dbuser = os.environ["dbuser"]
dbpassword = os.environ["dbpassword"]
dbhost = os.environ["dbhost"]

def database_connection():
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=dbuser,
            password=dbpassword,
            host=dbhost,
        )
        retorno = "Conectado com sucesso."
        status = 200
    except psycopg2.Error as e:
        retorno, status = f"Erro ao conectar no banco de dados: {e}", 500 

    return conn, retorno, status

def gerar_dados_fake_log_regressao_linear():
    # Conectar ao banco de dados
    conn, retorno, status = database_connection()

    if conn is not None:
        # Criar um cursor
        cur = conn.cursor()

        # Instanciar o Faker
        fake = Faker()

        # Gerar inserts aleatórios
        for _ in range(152):
            id_uuid = fake.uuid4()
            data_cotacao = fake.date_this_year()
            metodo = random.choice(['regressao_linear', 'clusterizacao_knn'])
            nome_cliente = fake.name()
            loan_limit = random.randint(1000, 10000)
            gender = random.choice([1, 2])
            loan_type = random.randint(1, 3)
            loan_purpose = random.randint(1, 3)
            credit_worthiness = random.randint(1, 3)
            open_credit = random.randint(1, 5)
            income = round(random.uniform(1000, 10000), 5)
            valor_predito = round(random.uniform(0, 1), 5)
            r2 = round(random.uniform(0, 1), 5)
            rmse = round(random.uniform(0, 1), 5)
            emprestimo_aprovado = random.choice([0, 1])

            # Executar o insert
            cur.execute(
                "INSERT INTO cotacoes (id_UUID, data_cotacao, metodo, nome_cliente, loan_limit, gender, loan_type, loan_purpose, credit_worthiness, open_credit, income, valor_predito, r2, rmse, emprestimo_aprovado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (id_uuid, data_cotacao, metodo, nome_cliente, loan_limit, gender, loan_type, loan_purpose, credit_worthiness, open_credit, income, valor_predito, r2, rmse, emprestimo_aprovado)
            )

        # Commit para confirmar as mudanças
        conn.commit()

        # Fechar o cursor e a conexão
        cur.close()
        conn.close()
    else:
        print(retorno)

gerar_dados_fake_log_regressao_linear()