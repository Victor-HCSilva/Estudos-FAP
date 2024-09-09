import streamlit as st
from func_conexao_ao_banco import conexao_ao_banco
from random import randint

def novo_numero():
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        
        if conexao:
            cursor.execute('''SELECT numero_da_conta FROM banco; ''')
            lista_de_numeros = list(range(10000, 100000, 1))  # Números possíveis de conta
            contas_existentes = [conta[0] for conta in cursor.fetchall()]  # Números de contas existentes
            t = len(contas_existentes)  # Número de contas existentes
            
            # Se houver contas criadas
            if t > 0:
                while t:
                    numero = lista_de_numeros[randint(0, len(lista_de_numeros)-1)]
                    if numero not in contas_existentes:
                        return numero  # Retornando um número aleatório que não está na lista
                    t -= 1
                    
            # Caso contrário, o primeiro número retornado é 11111
            else:
                return 11111
        
    except Exception as erro:
        st.error(f"Erro na geração do número: {erro}")

# Integração com Streamlit
def main():
    st.title("Sistema Bancário")

    menu = ["Possuo Conta", "Não Possuo Conta", "Gerar Novo Número de Conta", "Sair"]
    escolha = st.sidebar.selectbox("Menu", menu)

    # Se o usuário já possui conta
    if escolha == "Possuo Conta":
        numero_da_conta = st.number_input("Insira o número da conta", min_value=0, step=1)
        senha = st.text_input("Digite sua senha", type="password")
        # ... (resto do código para gerenciar a conta)

    # Se o usuário não possui conta
    elif escolha == "Não Possuo Conta":
        nome = st.text_input("Insira seu nome").title()
        saldo = 0
        tipo_de_conta = st.selectbox("Escolha o tipo de conta", ["Conta Corrente", "Conta Salário"])
        # ... (resto do código para criar a conta)

    # Gerar Novo Número de Conta
    elif escolha == "Gerar Novo Número de Conta":
        if st.button("Gerar Número"):
            numero = novo_numero()
            if numero:
                st.success(f"Novo número de conta gerado: {numero}")

    # Sair do sistema
    elif escolha == "Sair":
        st.write("Programa encerrado.")

if __name__ == '__main__':
    main()
