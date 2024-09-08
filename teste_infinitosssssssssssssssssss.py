from _funcoes_ import conexao_ao_banco, mostrar_id

def salvar_movimentacoes(tipo_de_operacao, _data_, saldo,id):
    try:
        #pequeno tratamento
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = """INSERT INTO movimentacoes (id_cliente, tipo_de_operacao,_data_,saldo)
                            VALUES (%s, %s, %s ,%s)"""
        
        values = (id, tipo_de_operacao,_data_,saldo)
        cursor.execute(executar, values)        
        conexao.commit()
        
        print(f'Salvo em: "movimentacoes"')
        
    except Exception as erro:
        print(f'\nErro ao mostrar histórico de movimentações: {erro}')
        
    finally:
        if conexao.is_connected():
            conexao.close()

numero = int(input('Numero: '))
salvar_movimentacoes('NC','2024-08-29',0,mostrar_id(numero_da_conta=numero,opcao='2'))