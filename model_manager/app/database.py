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

def grava_log(uuid_valor, data_cotacao, metodo, nome_cliente, loan_limit, Gender, loan_type, loan_purpose, Credit_Worthiness, open_credit, income, valor_predito, r2, rmse):
    conn = database_connection()[0]
    cursor = conn.cursor()

    try:
        query = f"insert into public.cotacoes(id_UUID, data_cotacao, metodo, nome_cliente, loan_limit, gender, loan_type, loan_purpose, credit_worthiness, open_credit, income, valor_predito, r2, rmse) values ('{uuid_valor}', '{data_cotacao}', '{metodo}', '{nome_cliente}', {loan_limit}, {Gender}, {loan_type}, {loan_purpose}, {Credit_Worthiness}, {open_credit}, {income}, {valor_predito}, {r2}, {rmse});"
        cursor.execute(query) 
        conn.commit()  # É necessário fazer commit apapp.run(host='0.0.0.0', port=5000, debug=True)ós a inserção
        retorno = "Emprestimo cadastrado com sucesso"
        status = 200
    except psycopg2.Error as e:
        retorno, status = f"Erro ao realizar a consulta: {e}", 500        

    cursor.close()
    conn.close()

    return retorno, status

def aprovar_emprestimo(uuid_valor, aprovado):
    conn = database_connection()[0]
    cursor = conn.cursor()

    try:
        query = f"update public.cotacoes set emprestimo_aprovado = {aprovado} where id_UUID = '{uuid_valor}';"
        cursor.execute(query)        
        conn.commit()  # É necessário fazer commit apapp.run(host='0.0.0.0', port=5000, debug=True)ós a inserção
        retorno = "Emprestimo alterado com sucesso"
        status = 200
    except psycopg2.Error as e:
        retorno, status = f"Erro ao realizar a consulta: {e}", 500        

    cursor.close()
    conn.close()

    return retorno, status

def busca_dados_data_drift(metodo):
    # Conectar ao banco de dados
    conn = database_connection()[0]
    cursor = conn.cursor()
 
    try:
        # Criar um cursor
        cur = conn.cursor()

        # Executar a consulta SQL
        cur.execute(f"SELECT * FROM public.cotacoes WHERE metodo = '{metodo}'")

        # Buscar os resultados da consulta
        dados = cur.fetchall()
        retorno = dados
        status = 200
    except psycopg2.Error as e:
        retorno, status = f"Erro ao realizar a consulta: {e}", 500        

    cursor.close()
    conn.close()

    return retorno, status