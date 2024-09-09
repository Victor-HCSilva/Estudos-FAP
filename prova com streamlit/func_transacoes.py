from func_conexao_ao_banco import conexao_ao_banco
from func_movimentacoes import movimentacoes

def transacoes( numero_da_conta:int, valor:float, tipo_de_transacao:str):  # tipo_de_transacao: 1 para depósito, 2 para saque
  
    conexao =conexao_ao_banco()
    cursor = conexao.cursor()

    if tipo_de_transacao=='deposito':#Depósito
        valor=valor
    elif tipo_de_transacao=='saque':#Saque
        valor = -valor
    try:
        # Atualiza o saldo adicionando o valor do depósito
        cursor.execute('UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;', (valor,numero_da_conta))
        conexao.commit()

        # Consulta novamente o saldo atualizado
        cursor.execute('SELECT saldo FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        saldo_atualizado = cursor.fetchone()[0]

        print(f'\nOperação realizada com sucesso.')
        print(f'Saldo atual: R${saldo_atualizado:.2f}.')

    except Exception as e:
        print(f"Ocorreu um erro ao processar o depósito: {e}")

#ok adiciona saldo positivo ou negativo à conta a depender da operacao (saque ou deposito)
if __name__=='__main__':
    #transacoes(tipo_de_transacao='deposito',valor = 100,numero_da_conta=11111)
    #movimentacoes(tipo_de_conta='conta_corrente',id = 1111,saldo=100, tipo_de_operacao='D')
    pass