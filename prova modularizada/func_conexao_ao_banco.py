import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()#O arquivo que contêm os dados está no arquivo ".env".

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

#Ok - 2024-09-07      
if __name__ == '__main__':
    #print(conexao_ao_banco())
    pass
    