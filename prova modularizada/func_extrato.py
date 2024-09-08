from func_conexao_ao_banco import conexao_ao_banco
def extrato(numero_da_conta):
    
    try:       
        conexao=conexao_ao_banco()
            
        if conexao.is_connected():    
            cursor = conexao.cursor()
            
            #buscando id        
            cursor.execute('select id_cliente from banco WHERE numero_da_conta = %s;',
                           (numero_da_conta,)
               
                        )    
    
            id = cursor.fetchone()[0]
            
            print(id)
            
            cursor = conexao.cursor()
            user = 'select * from movimentacoes where id_cliente = %s;'
            cursor.execute(user, (id,))        
            extrato_da_conta = cursor.fetchall()        
            
            if extrato_da_conta:
                for s in range(len(extrato_da_conta)):
                     print("ID:{}, Tipo de operação: {}, Data: {}, Saldo neste período: R${}".format(extrato_da_conta[s][0],extrato_da_conta[s][1],extrato_da_conta[s][3],extrato_da_conta[s][4]))
                        
                print('\nSaldo Atual: R${}'.format(extrato_da_conta[-1][-1]))
        
    except Exception as erro:   
        print(f'Erro ao gerar extrato: {erro}')

#É uma função delicada pórem funciona se bém chamada - ok - 2024-09-07, retorna histórico de tranfêrencias   
 
if __name__=='__main__':
    #extrato(62557)#numero da conta é necessário
    pass