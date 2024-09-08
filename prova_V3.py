from datetime import datetime
import  mysql.connector
from dotenv import load_dotenv
import os
def verificar_conta(numero_da_conta:int, nome:str):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        
        #Verificado nome e número de conta para verificar existêcia
        executar = """SELECT numero_da_conta,nome FROM banco_prova_fap_v3.banco;"""#è necessario retir os values             
        cursor.execute(executar)        
        
        for v in cursor.fetchall():
            if v[0] == numero_da_conta and v[1].lower().strip() == nome.lower().strip():
                return True
        else:
            #print('\nNão encontrado. Verifique se tudo foi digitado corretamente.')
            return False
                
    except Exception as erro:
        print(f'\nOcorreu um erro: {erro}')


def transferencia(n_conta_beneficiada, n_conta, valor):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        
        # Verificando se há saldo suficiente para a transferência
        saldo = float(mostrar_id(numero_da_conta=n_conta, opcao='1'))
        
        if saldo >= valor:
            # Retirando valor da conta remetente
            executar = """UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s"""
            values = (valor, n_conta)
            cursor.execute(executar, values)
            conexao.commit()
            
            # Adicionando valor à conta beneficiada
            executar = """UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s"""
            values = (valor, n_conta_beneficiada)
            cursor.execute(executar, values)
            conexao.commit()
            
            print('\nTransferência realizada com sucesso')
        
        else:
            print(f'\nAção inválida. Saldo insuficiente. Saldo atual: R${saldo:.2f}')
            return 
            
    except Exception as e:
        print(f'\nErro ao realizar a transferência. Verifique se tudo foi digitado corretamente. Detalhes: {e}')
        
    finally:
        # Fechando a conexão
        if conexao:
            cursor.close()
            conexao.close()
            
#tabelas usadas 
tabelas = '''
        create database banco_prova_fap_v3;
        use banco_prova_fap_v3;
        
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
#Funcção auxiliar, função que retorna ID ou Saldo da conta
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
 
#Função auxiliar, conexão ao banco de dados
def conexao_ao_banco():
    load_dotenv()
    
    try:
        conexao = mysql.connector.connect(
                host=os.environ['host'],
                database=os.environ['database'],
                user=os.environ['user'],
                password=os.environ['password']
            )
        return conexao
        
    except:
        print(f'Erro ao conectar ao banco de dados {Exception}')

#Mudança de nome ou número da conta
def mudanca(nome=None,numero_da_conta=None,id=None, tipo_de_alteracao=None):
    try:
        conexao = conexao_ao_banco()
            
        if conexao.is_connected():
            #criar uma conta
            
            if tipo_de_alteracao == '1':
                cursor = conexao.cursor()
                user = """UPDATE banco SET nome = %s WHERE (numero_da_conta =%s);
                                    """
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
            
#Extarto
def extrato(id):
    try:       
        conexao=conexao_ao_banco()
        
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
        
#criar uma conta
def criar_conta(data,nome,numero_da_conta,tipo_de_conta, saldo):
    try:
        conexao = conexao_ao_banco()
            
        if conexao.is_connected():
    
            cursor = conexao.cursor()
            user = """INSERT INTO banco (numero_da_conta, nome, tipo_de_conta,_data_, saldo)
                                VALUES (%s, %s, %s, %s,%s )"""
    
            user_dados = (numero_da_conta, nome, tipo_de_conta, data, saldo)
            cursor.execute(user, user_dados)
            conexao.commit()
                    
            print('\ncadastrado!')
                    
    except Exception as erro:
        print(f'Erro na inserção dos dados: {erro}')

#Depositar    
def depositar(numero_da_conta, valor):
    try:
        
        valor = float(valor)
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
    
        # Atualizando o saldo
        atualizar_saldo = 'UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;'
        cursor.execute(atualizar_saldo, (valor, numero_da_conta))
        conexao.commit()

        # Verificando o novo saldo
        consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
        cursor.execute(consulta_saldo, (numero_da_conta,))
        
        resultado = cursor.fetchone()
        novo_saldo = resultado[0]
        
        print('Saldo atualizado com sucesso. Saldo atual: R${}'.format(novo_saldo))
       
    except Exception as erro:
        print(f"Erro ao depositar: {erro}")
        
#Sacar
def sacar(numero_da_conta, valor):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        
        #Retirando valor
        atualizar_saldo = 'UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s;'
        cursor.execute(atualizar_saldo, (valor, numero_da_conta))
        conexao.commit()
    
        #Vendo salto atual
        consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
        cursor.execute(consulta_saldo, (numero_da_conta,))
        resultado = cursor.fetchone()

        if resultado:
            novo_saldo = resultado[0]
            print('\nSaldo atualizado com sucesso. Saldo atual: R${}'.format(novo_saldo))
            
        else:
            print('\nNúmero da conta não encontrado.')

    except Exception as erro:
        print(f"Erro ao sacar: {erro}")

#deletar conta
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

#Salvar movimentações
def salvar_movimentacoes(tipo_de_operacao, _data_, saldo,id):
    try:
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
        
#Menu
while True:
    try:
        DATA = str(datetime.now())
        MOVIMENTCOES = []
        print('\n1. Criar nova conta.')
        print('2. Depositar.')
        print('3. Sacar.')
        print('4. Extrato.')
        print('5. Apagar conta.')
        print('6. Realizar mudanças.')
        print('7. Transferência.')
        print('0. Cancelar.')

        opcao = input('Digite a opção escolhida: ')

        # Criar conta
        if opcao == '1':
            nome = input('Nome: ').title()
            numero_da_conta = int(input('Número da conta: '))

            while True:
                tipo_de_conta = input('Tipo de conta: 1-conta corrente 2-conta poupança: ')
                if tipo_de_conta == '1':
                    tipo_de_conta = 'conta_corrente'
                    break
                elif tipo_de_conta == '2':
                    tipo_de_conta = 'conta_poupanca'
                    break
            saldo = 0

            if verificar_conta(numero_da_conta=numero_da_conta, nome=nome):
                print('Já existe uma conta com este número, por favor tente outro.')
            else:
                criar_conta(data=DATA, nome=nome, numero_da_conta=numero_da_conta, tipo_de_conta=tipo_de_conta, saldo=saldo)

        # Depositar
        elif opcao == '2':
            valor = float(input('Valor que deseja depositar: '))
            numero_da_conta = int(input('Número da conta: '))
            nome = input(f"Insira o nome do titular da conta {numero_da_conta}: ")
            tipo_de_operacao = 'D'

            if valor > 0 and verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                depositar(numero_da_conta, valor)
                salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao, _data_=DATA, id=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'), saldo=mostrar_id(numero_da_conta=numero_da_conta, opcao='1'))
            else:
                print('\nInválido valor menor ou igual a zero.')

        # Sacar
        elif opcao == '3':
            numero_da_conta = int(input('Insira o número da conta: '))
            valor = float(input('Insira o valor que deseja sacar: '))
            nome = input('Insira o nome do titular da conta: ')

            if 0 < valor <= float(mostrar_id(numero_da_conta=numero_da_conta, opcao='1')) and verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                tipo_de_operacao = 'S'
                sacar(numero_da_conta=numero_da_conta, valor=valor)
                salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao, _data_=DATA, id=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'), saldo=mostrar_id(numero_da_conta=numero_da_conta, opcao='1'))
            else:
                print(f'Não é possível realizar esta operação. Seu saldo é de R${mostrar_id(opcao="1", numero_da_conta=numero_da_conta)}')

        # Extrato
        elif opcao == '4':
            numero_da_conta = int(input('\nInsira o número da conta: '))
            nome = input('Insira o nome: ')
            if verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                extrato(id=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'))

        # Excluir conta
        elif opcao == '5':
            numero_da_conta = int(input('Número da conta: '))
            nome = input('Nome do titular da conta: ')
            if verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                deletar(numero_da_conta, nome)

        # Mudanças de nome ou número de conta
        elif opcao == '6':
            print('1. Mudar nome')
            print('2. Número da conta')
            escolha = input('O que deseja mudar? ')

            if escolha == '1':
                nome = input('Insira o novo nome: ')
                numero_da_conta = input('Insira o Número da conta: ')
                if verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                    mudanca(nome=nome, numero_da_conta=numero_da_conta, tipo_de_alteracao=escolha)

            elif escolha == '2':
                numero_da_conta = input('Insira o novo Número da conta: ')
                id = input('Insira o id do cliente: ')
                mudanca(id=id, numero_da_conta=numero_da_conta, tipo_de_alteracao=escolha)

        # Transferência
        elif opcao == "7":
            n_conta_beneficiada = int(input('Insira o número da conta do beneficiário: '))
            n_conta = int(input('Insira o número da conta: '))
            valor = int(input('Insira o valor da transferência: '))

            if 0 < valor <= float(mostrar_id(opcao='1', numero_da_conta=n_conta)):
                if mostrar_id(opcao='1', numero_da_conta=n_conta_beneficiada):
                    transferencia(n_conta=n_conta, n_conta_beneficiada=n_conta_beneficiada, valor=valor)
                    salvar_movimentacoes(_data_=DATA, tipo_de_operacao="T", id=mostrar_id(opcao='2', numero_da_conta=n_conta), saldo=mostrar_id(opcao='1', numero_da_conta=n_conta))
                else:
                    print('Não existe uma conta com esse número')

        # Sair
        elif opcao == '0':
            print('Programa encerrado')
            break   

    except ValueError as e:
        print('\nVocê digitou algo incorreto, por favor repetir ação.')
        
    except Exception:
        print(f'\nOps aconteceu um imprevisto: {Exception}')
