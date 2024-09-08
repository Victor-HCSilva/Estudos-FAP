'''
INSERIR AS FUNÇÕES DE exibir extrato
NO CÓDIGO PRINCIPAL, OU SEJA, AJUSTAR AS VARIAVEIS NECESSÁRIAS
PARA QUALQUER OPERAÇÃO DAS OPÇÕES APRESENTADAS NO MENU
junto da criação da deleção a parte mais fácil

ADD:
- DELEÇÃO DE CONTA
- COLOCAR SALDO/ TIRAR SALDO

POR ENQUANTO É ISSO QUE QUERO FAZER(27-08-27)
'''


import  mysql.connector
#ok
def conexao_ao_banco():
    try:
        conexao = mysql.connector.connect(
                host='localhost',
                database='BANCO_PROVA_FAP_v1',
                user='root',
                password='V1ct0r_Hug@'
            )
    
        return conexao
        
    except:
        print(f'Erro ao conectar ao banco de dados {Exception}')
        
#ok   
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
        
#_______________________________________________________________        

#ok
def extrato(id):
    
    try:
        id = str(id,)
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        #executar = ("SELECT * FROM banco where id_cliente = %s;" )
        executar = (f"SELECT * FROM banco where id_cliente = {(id)};" )
        
        
        cursor.execute(executar)        
        print(f'\nExtrato do usuário de ID {id[0].replace(',','')}:')
        print(f'Saldo atual: {cursor.fetchall()[0][5]:.2f}\n')

        executar = (f"SELECT * FROM movimentacoes where id_cliente = {(id)};" )
        cursor.execute(executar)  
        
        for i in cursor.fetchall():
            print(f'Ação do tipo: {i[1]}, Data: {i[2]}, saldo neste período: {i[3]}')        
            
    except Exception as erro:
        print(f"Erro ao buscar extrato: {erro}")
        pass
        
    finally:
        if conexao.is_connected():
            conexao.close()
        
#ok
def depositar(cursor, id, valor):
    try:
        # Convertendo o ID e valor para os tipos corretos
        id = int(id)
        valor = float(valor)

        # Conexão com o banco de dados
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()

        # Buscando o saldo atual
        consulta_saldo = 'SELECT saldo FROM banco_prova_fap_v12 WHERE id_cliente = %s;'
        cursor.execute(consulta_saldo, (id,))
        resultado = cursor.fetchone()

        if resultado:
            saldo_atual = resultado[0]

            # Atualizando o saldo na tabela
            novo_saldo = saldo_atual + valor
            atualizar_saldo = 'UPDATE banco_prova_fap_v12 SET saldo = %s WHERE id_cliente = %s;'
            cursor.execute(atualizar_saldo, (novo_saldo, id))
            conexao.commit()

            print(f'Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}')
        else:
            print('ID do cliente não encontrado.')

    except Exception as erro:
        print(f"Erro ao depositar: {erro}")

    finally:
        if conexao:
            conexao.close()
    
def deletar(id):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = 'DELETE FROM banco_prova_fap_v10.banco WHERE id_cliente = %s;'
            
        cursor.execute(executar, (id,))  
        conexao.commit() 
        
        executar = 'DELETE FROM banco_prova_fap_v10.movimentacoes WHERE id_cliente = %s;'
            
        cursor.execute(executar, (id,))  
        conexao.commit() 
        print('Conta encerrada')
           
    except Exception as erro:
        print(f"Erro ao tentar excluir permanentemente a conta: {erro}")
            
    finally:
        if conexao.is_connected():
            conexao.close()
        
        
def mostrar_id(opcao, numero_da_conta):  # 1 retorna saldo, 2, retornar id
    try:
        opcao = str(opcao)
        numero_da_conta = str(numero_da_conta)
        conexao = conexao_ao_banco()
        
        with conexao.cursor() as cursor:
            consulta_sql = "SELECT * FROM banco WHERE numero_da_conta = %s;"
            cursor.execute(consulta_sql, (numero_da_conta,))
            
            resultado = cursor.fetchall()  # Armazenar o resultado da consulta

            if resultado:
                if opcao == '1':  # Se a opção for 1 e houver um resultado
                    return str(resultado[0][5])  # Retorna o saldo (coluna 5)
                elif opcao == '2':  # Se a opção for 2 e houver um resultado
                    return str(resultado[0][0])  # Retorna o ID
            else:
                print('Não encontrado')  # Caso contrário, imprime uma mensagem
        
    except Exception as erro:
        print(f'Erro ao retornar dados: {erro}') 
    
    finally:
        if conexao and conexao.is_connected():
            conexao.close()
 
#print(salvar_movimentacoes(cursor=conexao_ao_banco(), tipo_de_operacao='D',_data_= '2024-08-27',saldo=0,id=1))#
#print(f'\nExtrato:{extrato(cursor=conexao_ao_banco(), id=1)}')
#print(f'\nDepositar:{depositar(cursor=conexao_ao_banco(), id=1, valor=5)}')
#numero=input('Numero: ')
#print(mostrar_id())

#print(f'deletar: {deletar(id=mostrar_id(numero_da_conta=numero))}')

#tabelas No MySql 
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

def escolha():
    while True:
        print('\n1.Criar nova conta.')
        print('2.Depositar. ')
        print('3.Sacar.')
        print('4.Extrato')
        print('5.Apagar conta.')
        print('0.Cancelar. ')
        operacao = input('O que deseja fazer? ')

        if operacao == '1' or operacao == '2' or operacao == '3' or operacao == '4' or operacao == '5' or operacao == '6':
            return operacao
        
        else:
            print('Opção inválida')


class _Banco_():
    def __init__(self):
        pass
    
    def novo_usuario(self,tipo_de_conta ,nome, data,  saldo, numero_da_conta):
        self.tipo_de_conta = tipo_de_conta 
        self.nome = nome
        self.data = data
        self.saldo = saldo
        self.numero_da_conta = numero_da_conta
        
        try:
            conexao = conexao_ao_banco()
            
            if conexao.is_connected():
                #criar uma conta
                if 'q':
                    
                    cursor = conexao.cursor()
                    user = """INSERT INTO banco (numero_da_conta, nome, tipo_de_conta,_data_, saldo)
                                VALUES (%s, %s, %s, %s,%s )"""
                                #(tipo_de_conta ,nome, data,  saldo, numero_da_conta)
                    user_dados = (self.numero_da_conta, self.nome, self.tipo_de_conta, self.data, self.saldo)

                    cursor.execute(user, user_dados)
                    conexao.commit()
                    
                    print('\ncadastrado!')
                    
        except Exception as erro:
            print(f'Erro na inserção dos dados: {erro}')
            
        finally:
            if conexao.is_connected:
                conexao.close()
                
    def deletar(id=1):
        
        try:
            conexao = conexao_ao_banco()
            cursor=conexao.cursor()
            executar = 'DELETE FROM banco_prova_fap_v10.banco WHERE id_cliente = %s;'
                
            cursor.execute(executar, (id,))  
            conexao.commit() 
            
            executar = 'DELETE FROM banco_prova_fap_v10.movimentacoes WHERE id_cliente = %s;'
                
            cursor.execute(executar, (id,))  
            conexao.commit() 
            print('Conta encerrada')
            
        except Exception as erro:
            print(f"Erro ao tentar excluir permanentemente a conta: {erro}")
                
        finally:
            if conexao.is_connected():
                conexao.close()
        
    def depositar(self, id, valor):
        try:
            # Convertendo o ID e valor para os tipos corretos
            id = int(id)
            valor = float(valor)

            # Conexão com o banco de dados
            conexao = conexao_ao_banco()

            # Usando with para garantir o fechamento do cursor
            with conexao.cursor() as cursor:
                # Buscando o saldo atual
                consulta_saldo = 'SELECT saldo FROM banco WHERE id_cliente = %s;'
                cursor.execute(consulta_saldo, (id,))
                resultado = cursor.fetchone()

                if resultado:
                    saldo_atual = resultado[0]

                    # Atualizando o saldo na tabela
                    novo_saldo = float(saldo_atual) + valor
                    atualizar_saldo = 'UPDATE banco SET saldo = %s WHERE id_cliente = %s;'
                    cursor.execute(atualizar_saldo, (novo_saldo, id))
                    conexao.commit()

                    print(f'Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}')
                else:
                    print('ID do cliente não encontrado.')

        except Exception as erro:
            print(f"Erro ao depositar: {erro}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()

    def extrato(self,id):
        try:
            self.id = str(id)
            conexao = conexao_ao_banco()
            cursor=conexao.cursor()
            executar = ("SELECT * FROM banco where id_cliente = %s;" )
            
            inserir = (self.id,)
            
            cursor.execute(executar, inserir)        
            print(f'\nExtrato do usuário de ID {id[0].replace(',','')}:')
            print(f'Saldo atual: {cursor.fetchall()[0][5]:.2f}\n')
            
            executar = ("SELECT * FROM movimentacoes where id_cliente = %s;" )
            cursor.execute(executar,inserir )  
            
            for i in cursor.fetchall():
                print(f'Ação do tipo: {i[1]}, Data: {i[2]}, saldo neste período: {i[3]}')        
                
        except Exception as erro:
            print(f"Erro ao buscar extrato: {erro}")
            pass
            
        finally:
            if conexao.is_connected():
                conexao.close()
        
