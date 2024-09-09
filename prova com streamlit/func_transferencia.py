from func_conexao_ao_banco import conexao_ao_banco
from func_movimentacoes import movimentacoes
def transferencia(valor:float, numero_do_beneficiado:int, numero_da_conta:int):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT numero_da_conta FROM banco where numero_da_conta =  %s;",
                       (numero_do_beneficiado,) )
        
        existe = cursor.fetchone()

        if existe:        
            # Retirando valor da conta remetente
            executar = """UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s"""
            values = (valor, numero_da_conta)
            cursor.execute(executar, values)
            conexao.commit()

            # Adicionando valor à conta beneficiada
            
            executar = """UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s"""
            values = (valor, numero_do_beneficiado)
            cursor.execute(executar, values)
            conexao.commit()

            print('\nTransferência realizada com sucesso')
        else:
            return

    except Exception as e:
        print(f'\nErro ao realizar a transferência. Verifique se tudo foi digitado corretamente. Detalhes: {e}')

#ok - faz uma tranferencia de uma conta à outra, caso a conta exista.
if __name__=='__main__':
    #transferencia(valor=100,numero_da_conta=94562,numero_do_beneficiado=62557)
    #movimentacoes(tipo_de_conta='conta_corrente',id=3,tipo_de_operacao='94562->62557',saldo=1234)
    pass