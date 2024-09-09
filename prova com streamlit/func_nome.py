from func_conexao_ao_banco import conexao_ao_banco

def nome_do_cliente(numero_da_conta):
    try: 
        conexao = conexao_ao_banco()
        
        if conexao:
            cursor = conexao.cursor()
            executar = "SELECT nome FROM banco WHERE numero_da_conta = %s;)"
            values = ((numero_da_conta,))
            cursor.execute(executar, values)                    
            
            return cursor.fetchone()[0]

        else:
            print("Erro na conexão ao banco.")
            
    except Exception as erro:
        print(f'\nErro ao buscar nome: {erro}')
    
#ok - 2024-09-07. - Retorna uma string
if __name__=='__main__':
    #print(nome_do_cliente(123))    
    pass

