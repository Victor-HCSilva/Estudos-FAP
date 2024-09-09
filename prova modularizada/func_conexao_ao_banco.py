import mysql.connector
from dotenv import load_dotenv
import os
from pathlib import Path

# Defina o caminho completo para o arquivo .env
caminho_env = Path('C:/Users/victo/Desktop/.env')  # Usando barras normais ou duplas barras invertidas

# Carrega as variáveis do arquivo .env localizado na outra pasta
load_dotenv(dotenv_path=caminho_env)

def conexao_ao_banco():        
    try:
        conexao = mysql.connector.connect(
                host=os.environ['host'],
                database=os.environ['database'],
                user=os.environ['user'],
                password=os.environ['password']
            )
        return conexao
    except Exception as erro:
        print(f'\nErro ao conectar ao banco de dados: {erro}')

if __name__ == '__main__':
    conexao_ao_banco()
