
from datetime import datetime
import  mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

class Banco():
    #Data ja vém com valor dado pelo modulo datetime, ou seja não é necessario preenchelo em nenhum método.
    def __init__(self):#,tipo_de_operacao=None,nome=None,numero_da_conta=None,numero_do_beneficiado=None,id=None,tipo_de_conta=None, saldo=None,data=str(datetime.now()), valor=None):
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


    def verificar_conta(self, nome:str, numero_da_conta:int):
        self.nome = nome.title()
        self.numero_da_conta = numero_da_conta
        
        try:
            conexao = self.conexao_ao_banco()
            cursor = conexao.cursor()
            
            # Otimização: Adicionando cláusula WHERE para verificar a conta diretamente no banco
            executar = """SELECT numero_da_conta, nome FROM banco_prova_fap_v3.banco
                        WHERE numero_da_conta = %s AND nome = %s;"""
            cursor.execute(executar, (self.numero_da_conta, self.nome.lower().strip()))
            
            resultado = cursor.fetchone()
            if resultado:
                return True
            else:
                return False
                    
        except Exception as erro:
            print(f'\nOcorreu um erro: {erro}')

            
    #deletar            
    def deletar(self,numero_da_conta: int,nome:str):
        self.nome = nome
        self.numero_da_conta = numero_da_conta
        
        try:
            conexao = self.conexao_ao_banco()
            cursor=conexao.cursor()
            executar = 'DELETE FROM banco WHERE numero_da_conta = %s and nome = %s;'
                
            cursor.execute(executar, (self.numero_da_conta,self.nome))  
            conexao.commit() 
            
            print('Conta encerrada')
            
        except Exception as erro:
            print(f"Erro ao tentar excluir permanentemente a conta: {erro}")
            
    #depositar
    '''
    elif opcao == '3':
            valor = float(input('Valor que deseja sacar: '))
            numero_da_conta = int(input('Número da conta: '))
            nome = input(f"Insira o nome do titular da conta {numero_da_conta}: ")
            tipo_de_operacao = 'S'
            tipo_de_transacao = 2#2 para saque, 1 para depositar
            if valor > 0:
                if banco.verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                    banco.realizar_transacao(numero_da_conta=numero_da_conta, valor=valor, tipo_transacao=2)
                    banco.salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao, data=DATA, id=banco.encontrar_id(numero_da_conta=numero_da_conta, nome=nome), saldo=banco._saldo(numero_da_conta))
                else:
                    print('\nErro na transação.')
            else:
                print('\nInválido valor menor ou igual a zero.')
    
    '''
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
    def criar_conta(self,numero_da_conta:int,nome:str,data:str,saldo:float, tipo_de_conta):
        self.numero_da_conta = numero_da_conta
        self.data=data
        self.nome = nome
        self.saldo = saldo
        self.tipo_de_conta = tipo_de_conta
        try:
            conexao = self.conexao_ao_banco()
                
            if conexao.is_connected():
                cursor = conexao.cursor()
                user = """INSERT INTO banco (numero_da_conta, nome, tipo_de_conta,_data_, saldo)
                                    VALUES (%s, %s, %s, %s,%s )"""
                user_dados = (self.numero_da_conta, self.nome, self.tipo_de_conta, self.data, self.saldo)
                cursor.execute(user, user_dados)
                conexao.commit()
                        
                print('\nDados cadastrados, nova conta criada!')
        except Exception as erro:
            print(f'Erro na inserção dos dados: {erro}')

    def extrato(self, numero_da_conta: int,nome:str):
        self.numero_da_conta= numero_da_conta
        self.nome = nome
        try:       
            conexao=self.conexao_ao_banco()
            id = self.encontrar_id(numero_da_conta=self.numero_da_conta)
            
            if conexao.is_connected():    
                cursor = conexao.cursor()
                user = 'select * from movimentacoes where id_cliente = %s;'
                    
                cursor.execute(user, (id,))        
                extrato_da_conta = cursor.fetchall()
                    
                if extrato_da_conta:
                    for s in range(len(extrato_da_conta)):
                        print("\nID:{}, Tipo de movimentação: {}, Data: {}, Saldo neste período: R${}".format(extrato_da_conta[s][0],extrato_da_conta[s][1],extrato_da_conta[s][2],extrato_da_conta[s][3]))
                        
                    print('\nSaldo Atual: R${}'.format(extrato_da_conta[-1][3]))
            else:
                print('Não foi possível conectar ao banco de dados.')
                return

        except Exception as erro:
            print(f"Erro ao buscar extrato: {erro}")
            
    def encontrar_id(self, numero_da_conta):#RETORNA ID
        self.numero_da_conta = numero_da_conta
        
        try:
            conexao = self.conexao_ao_banco()
            cursor = conexao.cursor()
            
            consulta_sql = "SELECT * FROM banco WHERE numero_da_conta = %s;"
            cursor.execute(consulta_sql, (self.numero_da_conta))
            resultado = cursor.fetchone()  # Armazena o resultado da consulta

            if resultado:
                return str(resultado[0][0])  # Retorna o ID (coluna 0)
                
        except Exception as erro:
            print(f'Erro ao retornar dados: {erro}') 
        
        finally:
            if conexao and conexao.is_connected():
                conexao.close()                
            
    def transferencia(self, valor:float, numero_do_beneficiado:int, numero_da_conta:int, nome=str):
        self.valor = valor
        self.numero_da_conta = numero_da_conta
        self.numero_do_beneficiado = numero_do_beneficiado
        self.nome = nome
        try:
            conexao = self.conexao_ao_banco()
            cursor = conexao.cursor()
        
            # Retirando valor da conta remetente
            executar = """UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s"""
            values = (self.valor, self.numero_da_conta)
            cursor.execute(executar, values)
            conexao.commit()
                
                # Adicionando valor à conta beneficiada
            executar = """UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s"""
            values = (self.valor, self.numero_do_beneficiado)
            cursor.execute(executar, values)
            conexao.commit()
                
            print('\nTransferência realizada com sucesso')
            return 
                
        except Exception as e:
            print(f'\nErro ao realizar a transferência. Verifique se tudo foi digitado corretamente. Detalhes: {e}')
            
        finally:
            # Fechando a conexão
            if conexao:
                cursor.close()
                conexao.close()

    def mudar_nome(self, numero_da_conta:int,novo_nome:str):#'1'mudar nome
        self.novo_nome = novo_nome
        self.numero_da_conta = numero_da_conta
        try:
            conexao = self.conexao_ao_banco()
            cursor=conexao.cursor()
            
            #Verificado nome e número de conta para verificar existêcia
            executar = """UPDATE banco SET nome=%s  where numero_da_conta = %s ;"""
            cursor.execute(executar, (novo_nome, numero_da_conta,))        
            conexao.commit()
    
            executar = """SELECT nome from banco where numero_da_conta = %s ;"""
            cursor.execute(executar, (numero_da_conta,))   
            ok = cursor.fetchall()
            if ok:
                print('\nNome alterado com sucesso!')
                
        except Exception as erro:
            print(f'\nOcorreu um erro ao tentar realixar alteração.: {erro}')
            
    def _saldo(self, numero_da_conta):  # retorna saldo
        self.numero_da_conta = numero_da_conta
        
        try:
            conexao = self.conexao_ao_banco()
            if conexao:
                cursor = conexao.cursor()

                executar = 'SELECT saldo FROM banco_prova_fap_v3.banco WHERE numero_da_conta = %s;'
                cursor.execute(executar, (self.numero_da_conta,))
                
                resultado = cursor.fetchone()  # Utiliza fetchone() para pegar o primeiro resultado
                
                cursor.close()
                conexao.close()  # Fecha a conexão e o cursor após a execução.
                
                if resultado:
                    saldo = float(resultado[0])  # Extrai o saldo do resultado
                    return saldo
                else:
                    print('\nConta não encontrada. Verifique se o número da conta foi digitado corretamente.')
                    return False
            
            else:
                print("Erro na conexão ao banco.")
                return False
        
        except Exception as erro:
            print(f'\nOcorreu um erro: {erro}')
            return False
