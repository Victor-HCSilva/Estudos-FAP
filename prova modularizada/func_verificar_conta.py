from func_conexao_ao_banco import conexao_ao_banco

def verificar_conta(numero_da_conta:int):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()

        # Otimização: Adicionando cláusula WHERE para verificar a conta diretamente no banco
        cursor.execute('SELECT id_cliente from prova_fap.banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        resultado = cursor.fetchone()
        
        if resultado:
            return True
        else:
            return False

    except Exception as erro:
        print(f'\nOcorreu um erro ao verificar conta: {erro}')
#Verifica se alguma conta existe retornando True ou False
if __name__=='__main__':
    print(verificar_conta(11111))