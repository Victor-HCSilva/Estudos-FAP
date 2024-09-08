from datetime import datetime
import  mysql.connector
import os
from dotenv import load_dotenv


#04-09-2024
#tabelas usadas
tabelas = '''
        create database BANCO_PROVA_FAP_v3;
        use BANCO_PROVA_FAP_v3;
        
        create table if not exists banco (
            id_cliente INT AUTO_INCREMENT ,
            numero_da_conta int not null,
            nome varchar(100) not null,
            tipo_de_conta text not null,
            _data_ date not null,
            saldo decimal(65,2) not null ,
            PRIMARY KEY(id_cliente)
        );
        create table if not exists movimentacoes (
                id_cliente INT not null,
                tipo_de_operacao varchar(2) not null,
                _data_ date not null,
                saldo decimal(65,2) not null
                );
        '''

def mostrar_id(opcao, numero_da_conta):  # 1 retorna saldo, 2 retorna id
    try:
        opcao = str(opcao)
        numero_da_conta = str(numero_da_conta)
        conexao = conexao_ao_banco()
        
        with conexao.cursor() as cursor:
            consulta_sql = "SELECT * FROM banco WHERE numero_da_conta = %s;"
            cursor.execute(consulta_sql, (numero_da_conta,))
            
            resultado = cursor.fetchall()  # Armazena o resultado da consulta

            if resultado:
                if opcao == '1':  
                    return str(resultado[0][5])  # Retorna o saldo (coluna 5)
                elif opcao == '2':  
                    return str(resultado[0][0])  # Retorna o ID (coluna 0)
            else:
                print('Não encontrado')
        
    except Exception as erro:
        print(f'Erro ao retornar dados: {erro}') 
    
    finally:
        if conexao and conexao.is_connected():
            conexao.close()
            
load_dotenv()
def conexao_ao_banco():
    try:
        conexao = mysql.connector.connect(
                host='localhost',
                database='BANCO_PROVA_FAP_v3',
                user='root',
                password=os.environ['password'],
            )
    
        return conexao
        
    except:
        print(f'Erro ao conectar ao banco de dados {Exception}')

def mudanca(nome=None,numero_da_conta=None,id=None, tipo_de_alteracao=None):
    try:
        conexao = conexao_ao_banco()
            
        if conexao.is_connected():
            #criar uma conta
            
            if tipo_de_alteracao == '1':
                cursor = conexao.cursor()
                user = """UPDATE banco SET nome = %s WHERE (numero_da_conta =%s);
                                    """
                                    #(tipo_de_conta ,nome, data,  saldo, numero_da_conta)
                cursor.execute(user, (nome,numero_da_conta))
                conexao.commit()
                        
                print('\nMudança de nome realizada!')
                
            elif tipo_de_alteracao == '2':
                cursor = conexao.cursor()
                user = """UPDATE banco SET numero_da_conta = %s WHERE (id_cliente =%s);"""
                                    
                cursor.execute(user, (numero_da_conta,id))
                conexao.commit()
                print('\nMudança de número realizada!')
                
    except Exception as erro:
        print(f'Erro: {erro}')
            
    finally:
        if conexao.is_connected:
            conexao.close()



def extrato(id):
    conexao = None
    try:
        # Conexão com o banco de dados
        conexao = conexao_ao_banco()
        
        if conexao.is_connected():
            
            if conexao.is_connected():
            #criar uma conta
            
                    
                cursor = conexao.cursor()
                user = 'select * from banco where id_cliente = %s;'
                
                cursor.execute(user, (id,))
                saldo = cursor.fetchall()[0][5]
                if saldo:
                    print('Saldo:',saldo)
                    
                cursor = conexao.cursor()
                user = 'select * from movimentacoes where id_cliente = %s;'
                
                cursor.execute(user, (id,))
                
                for s in cursor.fetchall():
                    print(s)
            
        else:
            print('Não foi possível conectar ao banco de dados.')

    except Exception as erro:
        print(f"Erro ao buscar extrato: {erro}")

    finally:
        if conexao and conexao.is_connected():
            conexao.close()

def criar_conta(data,nome,numero_da_conta,tipo_de_conta, saldo):
    try:
        conexao = conexao_ao_banco()
            
        if conexao.is_connected():
            #criar uma conta
            
                    
            cursor = conexao.cursor()
            user = """INSERT INTO banco (numero_da_conta, nome, tipo_de_conta,_data_, saldo)
                                VALUES (%s, %s, %s, %s,%s )"""
                                #(tipo_de_conta ,nome, data,  saldo, numero_da_conta)
            user_dados = (numero_da_conta, nome, tipo_de_conta, data, saldo)
            cursor.execute(user, user_dados)
            conexao.commit()
                    
            print('\ncadastrado!')
                    
    except Exception as erro:
        print(f'Erro na inserção dos dados: {erro}')
            
    finally:
        if conexao.is_connected:
            conexao.close()
    
def depositar(numero_da_conta, valor):
    try:
        # Convertendo o valor para o tipo correto
        valor = float(valor)

        # Conexão com o banco de dados
        conexao = conexao_ao_banco()

        # Usando with para garantir o fechamento do cursor
        with conexao.cursor() as cursor:
            # Atualizando o saldo
            atualizar_saldo = 'UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;'
            cursor.execute(atualizar_saldo, (valor, numero_da_conta))
            conexao.commit()

            # Verificando o novo saldo
            consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
            cursor.execute(consulta_saldo, (numero_da_conta,))
            resultado = cursor.fetchone()

            if resultado:
                novo_saldo = resultado[0]
                print(f'Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}')
            else:
                print('Número da conta não encontrado.')

    except Exception as erro:
        print(f"Erro ao depositar: {erro}")

    finally:
        if conexao.is_connected():
            conexao.close()

def sacar(numero_da_conta, valor):
    try:
        # Convertendo o valor para o tipo correto
        valor = float(valor)

        # Conexão com o banco de dados
        conexao = conexao_ao_banco()

        # Usando with para garantir o fechamento do cursor
        with conexao.cursor() as cursor:
            # Atualizando o saldo
            atualizar_saldo = 'UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s;'
            cursor.execute(atualizar_saldo, (valor, numero_da_conta))
            conexao.commit()

            # Verificando o novo saldo
            consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
            cursor.execute(consulta_saldo, (numero_da_conta,))
            resultado = cursor.fetchone()

            if resultado:
                novo_saldo = resultado[0]
                print(f'Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}')
            else:
                print('Número da conta não encontrado.')

    except Exception as erro:
        print(f"Erro ao sacar: {erro}")

    finally:
        if conexao.is_connected():
            conexao.close()

def deletar(numero_da_conta, nome):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = 'DELETE FROM banco WHERE numero_da_conta = %s and nome = %s;'
            
        cursor.execute(executar, (numero_da_conta,nome))  
        conexao.commit() 
        
        print('Conta encerrada')
           
    except Exception as erro:
        print(f"Erro ao tentar excluir permanentemente a conta: {erro}")
            
    finally:
        if conexao.is_connected():
            conexao.close()

def salvar_movimentacoes(tipo_de_operacao, _data_, saldo,id):
    try:
        #pequeno tratamento
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = """INSERT INTO movimentacoes (id_cliente, tipo_de_operacao,_data_,saldo)
                            VALUES (%s, %s, %s ,%s)"""
        
        values = (id, tipo_de_operacao,_data_,saldo)
        cursor.execute(executar, values)        
        conexao.commit()
        
        print(f'Salvo em: "movimentacoes"')
        
    except Exception as erro:
        print(f'\nErro ao mostrar histórico de movimentações: {erro}')
        
    finally:
        if conexao.is_connected():
            conexao.close()

while True:
    DATA = str(datetime.now())
    MOVIMENTCOES = []
    print('\n1.Criar nova conta.')
    print('2.Depositar. ')
    print('3.Sacar.')
    print('4.Extrato')
    print('5.Apagar conta.')
    print('6.Realizar mudanças.')
    print('0.Cancelar. ')
    
    opcao = input('Digite a opção escolhida : ')
    if opcao == '1':
    
        nome = input('Nome: ').title()
        numero_da_conta = int(input('Numero da conta: '))
        while True:
            tipo_de_conta = input('Tipo de conta: 1-conta corrente 2-conta poupança: ')
            if tipo_de_conta == '1':
                tipo_de_conta = ('conta_corrente')
                break
            elif tipo_de_conta == '2':
                tipo_de_conta = ('conta_poupanca')
                break
        saldo = 0    
        criar_conta(data=DATA,nome=nome,numero_da_conta=numero_da_conta,tipo_de_conta=tipo_de_conta, saldo=saldo)

    #depositar
    elif opcao == '2':
        valor = int(input('Valor desejado: '))
        numero_da_conta = int(input('Número da conta: '))
        tipo_de_operacao = 'D'
        depositar(numero_da_conta,valor)
        #MOVIMENTACOES.append(numero_da_conta,tipo_de_operacao,DATA,saldo)
        salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao,_data_=DATA,id=mostrar_id(numero_da_conta=numero_da_conta,opcao='2'),saldo=mostrar_id(numero_da_conta=numero_da_conta,opcao='1'))
    #SACAR
    elif opcao=='3':
        
        valor = int(input('Valor desejado: '))
        numero_da_conta = int(input('Número da conta: '))
        saldo = 0#'verificar saldo'
        tipo_de_operacao = 'S'
        if valor > saldo:
            pass
            sacar(numero_da_conta=numero_da_conta,valor=valor)
            #MOVIMENTACOES.append(numero_da_conta,tipo_de_operacao,DATA,saldo)
            salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao,_data_=DATA,id=mostrar_id(numero_da_conta=numero_da_conta,opcao='2'),saldo=mostrar_id(numero_da_conta=numero_da_conta,opcao='1'))
    #extrat
    elif opcao=='4':
        numero_da_conta = int(input('Numero da conta: '))
        extrato(id=mostrar_id(numero_da_conta=numero_da_conta,opcao='2'))
        
    elif opcao=='5':
        numero_da_conta = int(input('Numero da conta: '))
        nome = input('Nome do titular da conta: ')
        deletar(numero_da_conta, nome)
    
    elif opcao=='6':
        while True:
            print('1.Mudar nome ')
            print('2.Número da conta')
            escolha = input('O que deseja mudar? ')
            if escolha == '1' or escolha== '2' :
                break
            
        if escolha == '1':
            nome=input('Insira o novo nome: ')
            numero_da_conta=input('Insira o Número da conta: ')
            mudanca(nome=nome, numero_da_conta=numero_da_conta, tipo_de_alteracao=escolha)
            
        elif escolha=='2':
            
            numero_da_conta = input('Insira o novo Número da conta: ')
            id=input('Insira o id do cliente: ')
            mudanca(id=id, numero_da_conta=numero_da_conta,tipo_de_alteracao=escolha)
        
        
    elif opcao=='0'        :
        break
    