from func_conexao_ao_banco import conexao_ao_banco

def exibir_nome(numero_da_conta:int):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        
        if conexao:
            cursor.execute(
                '''SELECT nome FROM banco where numero_da_conta = %s''', 
                (numero_da_conta,)
            )
            return cursor.fetchone()[0].title()
            
    except Exception as erro:
        pass
        
        
#ok - exibir nome
if __name__=='__main__':
    #print(exibir_nome(18344))
    pass