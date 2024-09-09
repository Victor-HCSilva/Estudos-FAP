from func_conexao_ao_banco import conexao_ao_banco
from datetime import datetime

def movimentacoes(saldo,tipo_de_operacao, tipo_de_conta,id ):  # tipo_transacao: 1 para depósito, 2 para saque
    data = str(datetime.now())
    conexao = conexao_ao_banco()
    cursor = conexao.cursor()

    try:
        # Atualiza o saldo adicionando o valor do depósito
        cursor.execute('Insert into movimentacoes (id_cliente, tipo_de_operacao, tipo_de_conta, _data_,saldo) VALUES (%s,%s,%s,%s,%s); ',
                       (id,tipo_de_operacao,tipo_de_conta,data,saldo)
                       )
        conexao.commit()
        
        print('\nRegistro salvo!')
        
    except Exception as e:
        print(f"\nOcorreu um erro ao registrar: {e}")

#ok adiciona saldo positivo ou negativo à conta a depender da operacao (saque ou deposito)
if __name__=='__main__':
   # movimentacoes(tipo_de_operacao='D',tipo_de_conta= 'conta_corrente',saldo=100., id=111)
    pass