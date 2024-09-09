import streamlit as st
from func_criar_nova_conta import criar_nova_conta
from func_deletar import deletar
from func_extrato import extrato
from func_id import encontrar_id
from func_transacoes import transacoes
from func_transferencia import transferencia
from func_saldo import _salario
from func_movimentacoes import movimentacoes
from func_verificar_senha import verificar_senha
from func_exibir_nome import exibir_nome

# Função principal
def main():
    st.title("Sistema Bancário")

    menu = ["Possuo Conta", "Não Possuo Conta", "Sair"]
    escolha = st.sidebar.selectbox("Menu", menu)

    # Se o usuário já possui conta
    if escolha == "Possuo Conta":
        numero_da_conta = st.number_input("Insira o número da conta", min_value=0, step=1)
        senha = st.text_input("Digite sua senha", type="password")

        if st.button("Entrar"):
            if senha == str(verificar_senha(numero_da_conta=numero_da_conta)):
                st.success(f"Bem-vindo, {exibir_nome(numero_da_conta)}")

                opcao_conta = st.selectbox("Escolha uma operação", ["Depositar", "Sacar", "Extrato", "Transferência", "Deletar Conta"])

                # Depósito
                if opcao_conta == "Depositar":
                    valor = st.number_input("Insira o valor que deseja depositar", min_value=0.0, step=0.01)
                    if st.button("Confirmar Depósito"):
                        if valor > 0:
                            transacoes(numero_da_conta=numero_da_conta, valor=valor, tipo_de_transacao='deposito')
                            saldo = _salario(numero_da_conta=numero_da_conta)
                            ID = encontrar_id(numero_da_conta=numero_da_conta)
                            movimentacoes(tipo_de_operacao='D', tipo_de_conta='conta_corrente', id=ID, saldo=saldo)
                            st.success("Depósito realizado com sucesso.")

                # Saque
                elif opcao_conta == "Sacar":
                    valor = st.number_input("Insira o valor que deseja sacar", min_value=0.0, step=0.01)
                    if st.button("Confirmar Saque"):
                        if _salario(numero_da_conta=numero_da_conta) >= valor > 0:
                            transacoes(numero_da_conta=numero_da_conta, valor=valor, tipo_de_transacao='saque')
                            saldo = _salario(numero_da_conta=numero_da_conta)
                            ID = encontrar_id(numero_da_conta=numero_da_conta)
                            movimentacoes(tipo_de_operacao='S', tipo_de_conta='conta_corrente', id=ID, saldo=saldo)
                            st.success("Saque realizado com sucesso.")
                        else:
                            st.error("Saldo insuficiente.")

                # Extrato
                elif opcao_conta == "Extrato":
                    st.text("Extrato: ")
                    extrato(numero_da_conta=numero_da_conta)

                # Transferência
                elif opcao_conta == "Transferência":
                    numero_do_beneficiado = st.number_input("Insira o número da conta beneficiada", min_value=0, step=1)
                    valor = st.number_input("Insira o valor que deseja transferir", min_value=0.0, step=0.01)
                    if st.button("Confirmar Transferência"):
                        if valor <= _salario(numero_da_conta):
                            transferencia(numero_da_conta=numero_da_conta, numero_do_beneficiado=numero_do_beneficiado, valor=valor)
                            id2 = encontrar_id(numero_do_beneficiado)
                            ID = encontrar_id(numero_da_conta=numero_da_conta)
                            movimentacoes(tipo_de_operacao=f'{ID}->{id2}', tipo_de_conta='conta_corrente', id=ID, saldo=_salario(numero_da_conta))
                            st.success("Transferência realizada com sucesso.")
                        else:
                            st.error("Saldo insuficiente.")

                # Deletar Conta
                elif opcao_conta == "Deletar Conta":
                    if st.button("Confirmar Deleção"):
                        if senha == str(verificar_senha(numero_da_conta=numero_da_conta)):
                            deletar(numero_da_conta=numero_da_conta)
                            st.success("Conta deletada com sucesso.")

    # Se o usuário não possui conta
    elif escolha == "Não Possuo Conta":
        nome = st.text_input("Insira seu nome").title()
        saldo = 0
        tipo_de_conta = st.selectbox("Escolha o tipo de conta", ["Conta Corrente", "Conta Salário"])
        
        if st.button("Criar Conta"):
            criar_nova_conta(nome=nome, saldo=saldo)
            numero_da_conta = st.number_input("Finalize digitando seu número da conta", min_value=0, step=1)
            ID = encontrar_id(numero_da_conta=numero_da_conta)
            movimentacoes(tipo_de_operacao='NC', tipo_de_conta=tipo_de_conta.lower(), id=ID, saldo=saldo)
            st.success("Conta criada com sucesso. Guarde seu número e senha.")

    # Sair do sistema
    elif escolha == "Sair":
        st.write("Programa encerrado.")

if __name__ == '__main__':
    main()
