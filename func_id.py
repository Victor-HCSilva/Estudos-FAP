import mysql.connector
from func_conexao_ao_banco import conexao_ao_banco

def _saldo(numero_da_conta):  # retorna saldo
    numero_da_conta = numero_da_conta
        
    try:
        conexao = conexao_ao_banco()
        
        if conexao:
            cursor = conexao.cursor()
            executar = 'SELECT saldo FROM banco_prova_fap_v3.banco WHERE numero_da_conta = %s;'
            cursor.execute(executar, (numero_da_conta,))
            resultado = cursor.fetchone()  # Utiliza fetchone() para pegar o primeiro resultado
            cursor.close()
            conexao.close()  # Fecha a conexão e o cursor após a execução.
                
            if resultado:
                return float(resultado[0])  # Extrai o saldo do resultado
            else:
                print('\nConta não encontrada. Verifique se o número da conta foi digitado corretamente.')
            
        else:
            print("Erro na conexão ao banco.")
        
    except Exception as erro:
        print(f'\nOcorreu ao tenatr acessar saldo: {erro}')
        
#ok - 2024-09-07, retorna um número tipo float, caso encontrado
if __name__=='__main__':
    #print(type(_saldo(123)),_saldo(123))#TIPO - Float
    pass