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
                database='BANCO_PROVA_FAP_v10',
                user='root',
                password='V1ct0r_Hug@'
            )
    
        return conexao
        
    except:
        print(f'Erro ao conectar ao banco de dados {Exception}')
        
#ok   
def mostrar_id(opcao='1', numero_da_conta=100):#1 ver id, 2, retornar id
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = ("SELECT * FROM banco where numero_da_conta = %s;" )
        numero_da_conta=(numero_da_conta,)
        
        cursor.execute(executar, numero_da_conta) 
        
        if opcao == '1':
            if cursor.fetchall():
                print(cursor.fetchall())
            else:
                return 'Não encontrado'
            
        elif opcao == '2':        
            if cursor.fetchall():
                return cursor.fetchall()
            else:
                return "Não encontrado"
        
    except Exception as erro:
        print(f'\nErro ao retornar ID do cliente: {erro}')
        
    finally:
        if conexao.is_connected():
            conexao.close()
        
#ok
def salvar_movimentacoes(cursor,tipo_de_operacao, _data_, saldo,id):
    try:
        #pequeno tratamento
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = """INSERT INTO movimentacoes (id_cliente, tipo_operecao,_data_,saldo)
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
def extrato(cursor, id):
    
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
    id = str(id)
    valor = str(valor)
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = 'UPDATE banco_prova_fap_v10.banco SET saldo = %s WHERE id_cliente = %s;'
        
        cursor.execute(executar, (valor, id))  
        conexao.commit() 
        
        executar = 'select * from banco  WHERE id_cliente = %s;'
        
        cursor.execute(executar, (id,))  
        novo_saldo = cursor.fetchall()[0][5]
        print(f'Saldo atual: {novo_saldo:.2f}')
        

    except Exception as erro:
        print(f"Erro ao buscar extrato: {erro}")
        
    finally:
        if conexao.is_connected():
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
        
        
def mostrar_id(opcao='1', numero_da_conta=400):#1 ver id, 2, retornar id
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = ("SELECT * FROM banco where numero_da_conta = %s;" )
        numero_da_conta=(numero_da_conta,)
        
        cursor.execute(executar, (numero_da_conta),)
        
        
        return cursor.fetchall()[0][0] if opcao=='1' else None
    
    except Exception as erro:
        print(f'erro ao retornar id: {erro}')        
        
#print(salvar_movimentacoes(cursor=conexao_ao_banco(), tipo_de_operacao='D',_data_= '2024-08-27',saldo=0,id=1))#
#print(f'\nExtrato:{extrato(cursor=conexao_ao_banco(), id=1)}')
#print(f'\nDepositar:{depositar(cursor=conexao_ao_banco(), id=1, valor=5)}')
#numero=input('Numero: ')
#print(mostrar_id())

#print(f'deletar: {deletar(id=mostrar_id(numero_da_conta=numero))}')