from func_conexao_ao_banco import conexao_ao_banco

def encontrar_id(numero_da_conta):#RETORNA ID
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
            
        cursor.execute("SELECT id_cliente FROM banco WHERE numero_da_conta = %s;", (numero_da_conta,))
        return cursor.fetchone()[0] 
       
    except:
        print(f'Erro ao retornar ID.')
        
#retorna id - ok - 2024-09-07    
if __name__=='__main__':
    #print(encontrar_id(62557))Enecessita do numero da conta
    pass