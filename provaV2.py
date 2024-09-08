#2 tabelinhas, tabela de cadastro | movimentação, data, numero da conta, tipo de operação "Deposito",  "saque",  "conta criada ", "conta deletada"

#menu: cadastrar, deposito, saque, listar,apagar
#Novas contas , movimentações de contas 
#numero, nome, data, tipo, saldo  <<<------------ cadastro
#contas(lista de dicionários) -->> [{}]

#qual a conta a depositar? mostrar o id para ver se existe, se existir qual o valor para ser depositado
#Seguindo  (o saldo atual) - (o que foi depositado).
#saque --->> há limite de pedido (R$1000), verificar se há saque 
#Extrato -->> ver o saldo da conta



'''
PARA VOCÊ (2024-08-23)!!!!

consertar a pesquisa de todos para que possam retornar tudo corretamente, 
não está nada sendo salvo. é possível colocar as operações em menos funções
apenas dependendo do tipo de operação[deixaria o código mais compacto], ademais 
as funcionalidades estão funcionando bém. Falta: deleção, tipos de conta, tratamnetos 
de erro, e salvamento de dados e operações [vide a nomeclatura adotada para tal].
E pode adicionar o que quiser a mais para ter o bonus do plus+++

'''

from datetime import datetime
import  mysql.connector
''''
d = datetime(2008,9,23)
f = datetime.now()
print(type(d),'d:',d, 'f:',f)
'''

#Banco de dados
def conexao_ao_banco():
    try:
        conexao = mysql.connector.connect(
                host='localhost',
                database='BANCO_PROVA_FAP_v10',
                user='root',
                password='V1ct0r_Hug@'
            )
    
        return conexao
        
    except:
        print(f'Erro ao conectar ao banco de dados {Exception}')
        
def novo_usuario(tipo_de_conta ,nome, data,  saldo, numero_da_conta):
    try:
        # Conectar ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            database='BANCO_PROVA_FAP_v10',
            user='root',
            password='V1ct0r_Hug@'
        )
        
        #tabelas No MySql 
        tabelas = '''
        create database BANCO_PROVA_FAP_v10;
        use BANCO_PROVA_FAP_v10;
        
        create table if not exists banco (
            id_cliente INT AUTO_INCREMENT ,
            numero_da_conta int not null,
            nome varchar(100) not null,
            tipo_de_conta text not null,
            _data_ date not null,
            saldo decimal(65,10) not null ,
            PRIMARY KEY(id_cliente)
        );
        create table if not exists movimentacoes (
                id_cliente INT,
                tipo_operecao varchar(2),
                _data_ date,
                saldo decimal(65,10),
                FOREIGN KEY (id_cliente) references banco(id_cliente)
        );	
        '''
        
        if conexao.is_connected():
            #criar uma conta
            if 'q':
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
        print('Conexão ao banco de dados encerrada')
        conexao.close()

#Vizualizar dados de toda a tabela banco
def vizualizar_banco():
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        cursor.execute("SELECT * FROM banco;")
        print('\nDados: \nID - NÚMERO - NOME - TIPO DE CONTA - DATA - SALDO ATUAL')
        for tarefa in cursor.fetchall():
            print(tarefa)
            
    except Exception as erro:
        print(f'\nErro ao vizualizar dados: {erro}')
        
    finally:
        print('\nConexão encerrada')
        conexao.close()

#Mostra: nome e ID, ou apenas retorna um id 

def mostrar_id(opcao='1', numero_da_conta=100):#1 ver id, 2, retornar id
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = ("SELECT * FROM banco where numero_da_conta = %s;" )
        numero_da_conta=(numero_da_conta,)
        
        cursor.execute(executar, numero_da_conta) 
        
        if opcao == '2':
            for dados in cursor.fetchall():
                print('ID:',dados[0],', Nome:',dados[2] )
            
        else:        
            return cursor.fetchall()[0][0]
        
    except Exception as erro:
        print(f'\nErro ao vizualizar dados: {erro}')
        
    finally:
        print('\nConexão encerrada')
        conexao.close()
    

#Vizualizar dados de um usuario    
def extrato(cursor, id):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = ("SELECT * FROM banco where id_cliente = %s;" )
        
        id = (id,)
        cursor.execute(executar, id)        
        print(f'\nExtrato do usuário de ID {id}:')
        print('------------------------------------------------')
        print(f'Saldo atual: {cursor.fetchall()[0][5]:.2f}')
    
    except Exception as erro:
        print(f'\nErro ao vizualizar usuário (id-{id}): {erro}')
        
    finally:
        print('\nConexão encerrada')
        conexao.close()
    

#Salvar movimentações
def salvar_movimentacoes(cursor,tipo_de_operacao, _data_, saldo,id):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = """INSERT INTO movimentacoes (id_cliente, tipo_operecao,_data_,saldo)
                            VALUES (%s, %s, %s ,%s)"""
        
        values = (id, tipo_de_operacao,_data_,saldo)
        cursor.execute(executar, values)        
        conexao.commit()
        
        print(f'\nOperação salva')
        
    except Exception as erro:
        print(f'\nErro ao mostrar histórico de movimentações: {erro}')
        
    finally:
        print('\nConexão encerrada')
        conexao.close()
       
def escolha():
    while True:
        print('\n1.Cadastrar nova conta.')
        print('2.Depositar. ')
        print('3.Sacar.')
        print('4.Extrato')
        print('5.Apagar conta.')
        print('6.Cancelar. ')
        operacao = input('O que deseja fazer? ')

        if operacao == '1' or operacao == '2' or operacao == '3' or operacao == '4' or operacao == '5' or operacao == '6':
            return operacao
        
        else:
            print('Opção inválida')
            
def menu():
    cadastro=[]
    try:
        movimentacao = True

        while movimentacao:
            
            operacao = escolha()
            
            #escolhendo o tipo de conta
            if operacao == '1':
                while True:
                    tipo_de_conta = ('conta_corrente','conta_salario','conta_poupanca', 'conta_pagamento')
                    print('\nTipo de conta:\n1.conta corrente\n2.conta salário\n3.conta poupança\n4.conta pagamento')
                    tipo = int(input('Escolha: '))
                    tipo_de_conta = tipo_de_conta[tipo-1]
                    
                    if 0 < tipo < 6:                    
                        break
                    print(f'Escolha Inválida: {tipo}')
    
                numero_da_conta = float(input('Número da conta: '))
                nome = input('Insira o nome: ').title()
                data = str(datetime.now())
                saldo = 0
                #E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                tipo_de_operacao='NC'
                
                novo_usuario(tipo_de_conta=tipo_de_conta,nome=nome,data=data,saldo=saldo,numero_da_conta=numero_da_conta)
                salvar_movimentacoes(cursor=conexao_ao_banco(), tipo_de_operacao=tipo_de_operacao,_data_=data,saldo=saldo,id=mostrar_id(numero_da_conta=numero_da_conta, opcao='1'))
                   
            #depositar
            elif operacao == '2':
                #parâmetros(numero_conta,dados, deposito)
                if cadastro:
                    print('Oi no 2')
                    numero_conta = int(input('numero da conta: '))
                    deposito = float(input('Insira o valor que deseja depositar:'))
                    dados = cadastro   
                    tipo_de_operacao='D'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                    
                    ##_movimentacao_(data, numero_conta, tipo_de_operacao)   
                     
                    for s in range(len(dados)):
                        print(f'Comparações: {dados[s]['numero']} e {numero_conta}')
                        
                        if dados[s]['numero'] == numero_conta:
                            dados[s]['saldo']+=deposito
                            
                            print(f'Saldo atual: {dados[s]['saldo']}')
                            msg='Encontrado!'
                            break
                        
                        else:
                            msg='Não encontrado'
                            
                    print(msg)                    
    
            #sacar
            elif operacao == '3':
                if cadastro:
                    tipo_de_operacao='S'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                    numero_conta = int(input('Número: '))
                    tipo_de_operacao = 'D'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                    saque_quantidade = float(input('Valor que deseja sacar: '))
                    dados = cadastro
                    #_movimentacao_(data, numero_conta, tipo_de_operacao)
                    for s in range(len(dados)):
                        print(f'Comparações: {dados[s]['numero']} e {numero_conta}')
                        
                        if dados[s]['numero'] == numero_conta:
                            msg=('Encontrado')
                            
                            if (dados[s]['saldo']- saque_quantidade) >= 0:
                                dados[s]['saldo']-= saque_quantidade
                                print(f'Saldo atual: {dados[s]['saldo']}')
                                break
                            else:
                                msg='Encontrado, pórem a ação não pode ser feita'
                                print('Não é possível realizar a operação')
                                break
                        else:
                            msg ='Não encontrado'
                            
                    print(msg)
                else:
                    print('Não há nenhum registro')

            #Extrato
            elif operacao== '4':
                numero_da_conta = int(input('Insira o número da conta: '))
                
                extrato(cursor=conexao_ao_banco(),id=mostrar_id(numero_da_conta=numero_da_conta, opcao='1'))
                    
            #apagar conta
            elif operacao == '5':
        
                if cadastro:
                    numero_conta = int(input('Número: '))
                    dados = cadastro
                    tipo_de_operacao = 'AC'
                    #_movimentacao_(data, numero_conta, tipo_de_operacao)
                    
                    for s in range(len(dados)):
                        print(f'Comparações: {dados[s]['numero']} e {numero_conta}')
                        
                        if dados[s]['numero'] == numero_conta:
                            msg='Deletado!'
                            dados.remove(dados[s])
                            break
                        else:
                            msg='Não encontrado'
                            
                    print(msg)  
                                     
                else:
                    print('Ainda não há nenhum registro')
                    
            elif operacao== '6':
                movimentacao = False
 
    except Exception as erro:
        print(f'Erro ao realizar operação, à devs: {erro}')

    finally:
        print('Operação encerrada')

if __name__ =='__main__' :
    menu()

