from func_conexao_ao_banco import conexao_ao_banco

def mudar_nome(numero_da_conta:int,novo_nome:str):#'1'mudar nome
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
            
        #Mudando nome
        executar = """UPDATE banco SET nome=%s  where numero_da_conta = %s ;"""
        cursor.execute(executar, (novo_nome.title(), numero_da_conta,))        
        conexao.commit()
        
        #buscando nome
        executar = """SELECT nome from banco where numero_da_conta = %s ;"""
        cursor.execute(executar, (numero_da_conta,))   
        
        if cursor.fetchall():
            print('\nNome alterado com sucesso!')
            
    except Exception as erro:
        print(f'\nOcorreu um erro ao tentar realixar alteração.: {erro}')

#Ok - 2024-09-07. Muda o nome de um usuario, usando o método title()
if __name__=='__main__':
    print(mudar_nome(123,'teste'))
    pass