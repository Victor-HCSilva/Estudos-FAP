from _funcoes_ import conexao_ao_banco
import matplotlib.pyplot as plt
import streamlit as st

def faze(numero_da_conta):
    try:
        conexao = conexao_ao_banco()

        # Operação 1
        cursor = conexao.cursor()
        cursor.execute('SELECT id_cliente FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))

        # Obter o resultado da consulta
        resultado = cursor.fetchone()

        # Verificar se a conta foi encontrada
        if resultado:
            id_cliente = resultado[0]

            # Operação 2
            cursor = conexao.cursor()
            cursor.execute('SELECT data, saldo FROM prova_fap.movimentacoes WHERE id_cliente = %s ;', (id_cliente,))

            # Obter o resultado da consulta (o saldo)
            movimentacoes = cursor.fetchall()
            print(movimentacoes)
            # Verificar se o saldo foi encontrado
            if movimentacoes:
                datas = [mov[0] for mov in movimentacoes]
                saldos = [mov[1] for mov in movimentacoes]

                # Criar o gráfico
                fig, ax = plt.subplots()
                ax.plot(datas, saldos)
                ax.set_xlabel('Data')
                ax.set_ylabel('Saldo')
                ax.set_title(f'Saldo da Conta {numero_da_conta}')

                # Exibir o gráfico no Streamlit
                st.pyplot(fig)

            else:
                st.write("Saldo não encontrado para este cliente.")
                
    except:
        pass
if __name__=='__main__':
    faze(18344)