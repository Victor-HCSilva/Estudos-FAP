
from dotenv import load_dotenv
import os
import mysql.connector
load_dotenv()

class T:
    def __init__(self) -> None:
        pass    
        self.nome = None
        self.numero_da_conta = None
        self.valor = None
        
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

    def realizar_transacao(self, numero_da_conta:int, valor:float, tipo_transacao:int):  # tipo_transacao: 1 para depósito, 2 para saque
        self.valor = valor
        self.numero_da_conta = numero_da_conta
        self.tipo_transacao = tipo_transacao
        
        try:
            conexao = self.conexao_ao_banco()
            cursor = conexao.cursor()
            
            if tipo_transacao == 1:
                try:
                    # Depósito
                    consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
                    cursor.execute(consulta_saldo, (self.numero_da_conta,))
                    saldo_atual = cursor.fetchone()[0]
                    
                    # Atualiza o saldo adicionando o valor do depósito
                    atualizar_saldo = 'UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;'
                    cursor.execute(atualizar_saldo, (self.valor, self.numero_da_conta))
                    conexao.commit()
                    
                    # Consulta novamente o saldo atualizado
                    cursor.execute(consulta_saldo, (self.numero_da_conta,))
                    saldo_atualizado = cursor.fetchone()[0]

                    print(f'\nO valor de R${self.valor:.2f} foi inserido na conta {self.numero_da_conta} com sucesso.')
                    print(f'Saldo atual: R${saldo_atualizado:.2f}.')

                except Exception as e:
                    print(f"Ocorreu um erro ao processar o depósito: {e}")
                finally:
                    return
    
            elif tipo_transacao == 2:
                try:
                    # Saque: Verifica saldo antes de sacar
                    consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
                    cursor.execute(consulta_saldo, (self.numero_da_conta,))
                    saldo_atual = cursor.fetchone()[0]

                    if saldo_atual >= self.valor:
                        # Atualiza o saldo subtraindo o valor do saque
                        atualizar_saldo = 'UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s;'
                        cursor.execute(atualizar_saldo, (self.valor, self.numero_da_conta))
                        conexao.commit()

                        # Imprime o saldo atualizado diretamente
                        saldo_atual = float(saldo_atual)- self.valor
                        print(f"O valor de R${self.valor} foi retirado. Saldo atual: R${saldo_atual}")

                    else:
                        print("Saldo insuficiente para realizar o saque.")

                except Exception as e:
                    print(f"Ocorreu um erro ao processar a transação: {e}")
                finally:
                    return

        except:
            pass                   
                    
c= T()
print(c.realizar_transacao(numero_da_conta=123,valor=100.0,tipo_transacao=1))