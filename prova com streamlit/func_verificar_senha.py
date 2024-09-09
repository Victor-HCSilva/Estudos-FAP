from func_conexao_ao_banco import conexao_ao_banco

def verificar_senha(numero_da_conta: int):  # tipo_de_transacao: 1 para depósito, 2 para saque
    conexao =conexao_ao_banco()
    cursor = conexao.cursor()
    
    try:
        cursor.execute('SELECT numero_da_conta, senha FROM banco WHERE numero_da_conta = %s;', (numero_da_conta, ))
        return cursor.fetchone()[-1]
    
    except Exception as e:
        print(f"Ocorreu um erro ao processar o depósito: {e}")

#verifica senha do usuraio
if __name__=='__main__':
    
    '''senha = int(input('Insira senha: '))
    numero = int(input('Insira o número da conta'))
    if senha == verificar_senha(senha=senha,numero_da_conta=numero):
        print('Ok bém vindo')'''
