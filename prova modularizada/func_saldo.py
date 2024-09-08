from func_conexao_ao_banco import conexao_ao_banco

def _salario(numero_da_conta: int):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        cursor.execute('SELECT saldo FROM banco WHERE numero_da_conta = %s;'
                       , (numero_da_conta,))  
        
        return cursor.fetchone()[0]

    except Exception as erro:
        print(f"Erro ao tentar retornar saldo: {erro}")

#ok , retorna o saldo
if __name__=='__main__':
    #print(_salario(62557))
    pass