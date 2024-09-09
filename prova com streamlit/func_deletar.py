from func_conexao_ao_banco import conexao_ao_banco

def deletar(numero_da_conta: int):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        cursor.execute('DELETE FROM banco WHERE numero_da_conta = %s;'
                       , (numero_da_conta,))  
        conexao.commit() 
        print('Conta encerrada')

    except Exception as erro:
        print(f"Erro ao tentar excluir permanentemente a conta: {erro}")

#deleta uma conta apartir do número dela
if __name__=='__main__':
    #deletar(62557)
    pass