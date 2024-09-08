from class_banco import Banco
from datetime import datetime
import  mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

banco = Banco()
class M:
    def __init__(self) -> None:
         pass
        
    def conexao_ao_banco(self):        
        try:
            conexao = mysql.connector.connect(
                    host=os.environ['host'],
                    database=os.environ['database'],
                    user=os.environ['user'],
                    password=os.environ['password']
                )
            return conexao
        except mysql.connector.Error as erro:
            print(f'Erro ao conectar ao banco de dados: {erro}')

     
    def salvar_movimentacoes(self, tipo_de_operacao: str, data: str, saldo: float, numero_da_conta):
        self.saldo = saldo
        self.data = data
        self.tipo_de_operacao = tipo_de_operacao
        self.id = self.encontrar_id(numero_da_conta=numero_da_conta)
        
        try:
            conexao = self.conexao_ao_banco()
            if conexao:
                cursor = conexao.cursor()
                executar = """INSERT INTO movimentacoes (id_cliente, tipo_de_operacao, _data_, saldo)
                            VALUES (%s, %s, %s, %s)"""
                values = (self.id, self.tipo_de_operacao, self.data, self.saldo)
                cursor.execute(executar, values)        
                conexao.commit()
                cursor.close()
                conexao.close()  # Fecha a conexão e o cursor após a execução.
                
                print(f'Salvo em: "movimentacoes"')
            else:
                print("Erro na conexão ao banco.")
            
        except Exception as erro:
            print(f'\nErro no salvamento da movimentação: {erro}')
    
    def encontrar_id(self, numero_da_conta):#RETORNA ID
        self.numero_da_conta = numero_da_conta
        
        try:
            conexao = self.conexao_ao_banco()
            cursor = conexao.cursor()
            
            consulta_sql = "SELECT id_cliente FROM banco WHERE numero_da_conta = %s;"
            cursor.execute(consulta_sql, (self.numero_da_conta, ))
            resultado = cursor.fetchone()[0]  # Armazena o resultado da consulta

            if resultado:
                return resultado  # Retorna o ID (coluna 0)
                
        except Exception as erro:
            print(f'Erro ao retornar dados: {erro}') 
        
        finally:
            if conexao and conexao.is_connected():
                conexao.close()          
          
m = M()
print(m.salvar_movimentacoes(numero_da_conta=123,tipo_de_operacao='TT', data=str(datetime.now()),saldo=0))#self, tipo_de_operacao: str, data: str, saldo: float)''''''''':
