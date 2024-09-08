import mysql.connector
import os 
from dotenv import load_dotenv

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

'''def trasferencia(n_conta_beneficiada,n_conta, valor):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        
        #verificando se há saldo para a trasferência
        saldo = float(mostrar_id(numero_da_conta=n_conta,opcao='1'))
        
        if saldo >= valor:           
        #Retirando valor(saldo=saldo-valor)
            executar = """UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s;'
                                VALUES (%s, %s)"""       #è necessario retir os values             
            values = (valor,n_conta )
            cursor.execute(executar, values)        
            conexao.commit()
            
        #adionando valor à benificiada(saldo=saldo+valor)
            executar = """UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;'
                                VALUES (%s, %s)"""#è necessario retir os values
            
            values = (valor,n_conta_beneficiada )
            cursor.execute(executar, values)        
            conexao.commit()
            
            print(f'\nTransfeêecia realizada com sucesso')
            
        else:
            print(f'\nAção inválida não há saldo suficiente. Saldo atual: R${saldo}')
            return 
    except:
        print(f'\nErro ao realizar Trasnfrêcia verifique se tudo foi digitado corretamente.')'''
        
        
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
            print('\nNão encontrado. Verifique se tudo foi digitado corretamente.')
            return False
                
    except Exception as erro:
        print(f'\nOcorreu um erro: {erro}')
        
        
def tipo_conta(numero_da_conta):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        
        executar = """SELECT tipo_de_conta, numero_da_conta, nome FROM banco_prova_fap_v3.banco;"""#è necessario retir os values             
        cursor.execute(executar)        
        
        for v in cursor.fetchall():
            if v[1] == numero_da_conta:
                return v[0], 
        else:
            print('\nNão encontrado :(. Verifique se tudo foi digitado corretamente.')
            return False
                
    except Exception as erro:
        print(f'\nOcorreu um erro: {erro}')
        
def _saldo(numero_da_conta):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        
        executar = """SELECT saldo FROM banco_prova_fap_v3.banco where numero_da_conta = %s;"""#é necessario retir os values             
        cursor.execute(executar, (numero_da_conta,))        
        
        saldo = cursor.fetchall()[0][0]
        if saldo:
            return float(saldo)
        else:
            print('\nNão encontrado :(. Verifique se tudo foi digitado corretamente.')
            return False
                
    except Exception as erro:
        print(f'\nOcorreu um erro: {erro}')

print(_saldo(100))
