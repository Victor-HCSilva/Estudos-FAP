from datetime import datetime
from func_conexao_ao_banco import conexao_ao_banco
from func_novo_numero import novo_numero
from func_senha import _senha

def criar_nova_conta(nome:str,saldo:float):
    try:
        numero_da_conta = novo_numero()
        senha = _senha()
        data = str(datetime.now())
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        
        if conexao:
            cursor.execute(
                '''INSERT INTO banco (numero_da_conta, nome,_data_, saldo, senha)
                                        VALUES (%s, %s, %s, %s,%s )''', 
                (numero_da_conta,nome,data,saldo, senha)
            )
            conexao.commit()
            cursor.close()
            conexao.close()
            
            print(f'\nConta criada com sucesso!')
            print('Veja os dados da conta: ')
            print(f'Nome: {nome.title()}, Senha: {senha}, Número da conta: {numero_da_conta}, Saldo: R${saldo}')
            
    except Exception as erro:
        print(f'Erro na criação da conta: {erro}')
        
        
#ok - insere na tabela uma nova conta
if __name__=='__main__':
    #criar_nova_conta(nome='Rogério',saldo=0,)
    pass