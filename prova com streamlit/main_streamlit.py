import os
from pathlib import Path
from random import randint
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
#[theme]

# Funções auxiliares de conexão e lógica de banco de dados

def conexao_ao_banco():
    try:
        conexao = mysql.connector.connect(
            host=os.environ['host'],
            database=os.environ['database'],
            user=os.environ['user'],
            password=os.environ['password']
        )
        return conexao
    except Exception as erro:
        st.error(f'\nErro ao conectar ao banco de dados: {erro}')
        return None

def novo_numero():
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute('SELECT numero_da_conta FROM banco;')
        contas_existentes = [conta[0] for conta in cursor.fetchall()]
        numero = randint(10000, 99999)
        while numero in contas_existentes:
            numero = randint(10000, 99999)
        return numero
    except Exception as erro:
        st.error(f"Erro na geração do número: {erro}")

def verificar_senha(numero_da_conta: int):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute('SELECT senha FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        return cursor.fetchone()[0]
    except Exception as e:
        st.error(f"Ocorreu um erro ao verificar a senha: {e}")
        return None

def exibir_nome(numero_da_conta: int):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute('SELECT nome FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        return cursor.fetchone()[0].title()
    except Exception as erro:
        st.error(f"Erro ao exibir nome: {erro}")
        return None

def _salario(numero_da_conta: int):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute('SELECT saldo FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        return cursor.fetchone()[0]
    except Exception as erro:
        st.error(f"Erro ao retornar saldo: {erro}")
        return None

def encontrar_id(numero_da_conta: int):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute('SELECT id_cliente FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        return cursor.fetchone()[0]
    except Exception as erro:
        st.error(f"Erro ao retornar ID: {erro}")
        return None

def movimentacoes(saldo, tipo_de_operacao, tipo_de_conta, id_cliente):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        data = str(datetime.now())
        cursor.execute('INSERT INTO movimentacoes (id_cliente, tipo_de_operacao, tipo_de_conta, _data_, saldo) VALUES (%s, %s, %s, %s, %s);', 
                       (id_cliente, tipo_de_operacao, tipo_de_conta, data, saldo))
        conexao.commit()
        st.success('Registro salvo!')
    except Exception as erro:
        st.error(f"Erro ao registrar movimentação: {erro}")

def transacoes(numero_da_conta, valor, tipo_de_transacao):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        
        if tipo_de_transacao == 'deposito':
            valor = valor
        elif tipo_de_transacao == 'saque':
            valor = -valor
            
        cursor.execute('UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;', (valor, numero_da_conta))
        conexao.commit()
        cursor.execute('SELECT saldo FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        saldo_atualizado = cursor.fetchone()[0]
        st.success(f'Operação realizada com sucesso. Saldo atual: R${saldo_atualizado:.2f}.')
        
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a transação: {e}")

def transferencia(valor, numero_do_beneficiado, numero_da_conta):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT numero_da_conta FROM banco WHERE numero_da_conta = %s;", (numero_do_beneficiado,))
        existe = cursor.fetchone()
        
        if existe:
            cursor.execute("UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s;", (valor, numero_da_conta))
            cursor.execute("UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;", (valor, numero_do_beneficiado))
            conexao.commit()
            st.success('Transferência realizada com sucesso.')
            return True
        else:
            st.error("Conta beneficiada não encontrada.")
            return False
            
    except Exception as e:
        st.error(f'Erro ao realizar a transferência: {e}')

def deletar(numero_da_conta):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        conexao.commit()
        st.success('Conta deletada com sucesso.')
    except Exception as erro:
        st.error(f"Erro ao tentar excluir conta: {erro}")

def extrato(numero_da_conta):
    try:
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        cursor.execute('SELECT id_cliente FROM banco WHERE numero_da_conta = %s;', (numero_da_conta,))
        id_cliente = cursor.fetchone()[0]
        cursor.execute('SELECT * FROM movimentacoes WHERE id_cliente = %s;', (id_cliente,))
        extrato_da_conta = cursor.fetchall()
        
        if extrato_da_conta:
            for registro in extrato_da_conta:
                st.text(f"ID: {registro[0]}, Tipo de operação: {registro[1]}, Data: {registro[3]}, Saldo neste período: R${registro[4]}")
            st.text(f'\nSaldo Atual: R${extrato_da_conta[-1][-1]}')
            
    except Exception as erro:
        st.error(f'Erro ao gerar extrato: {erro}')

# Interface Streamlit
import streamlit as st
from dotenv import load_dotenv

def main():
    st.title("Sistema Bancário simples")
    
    # Inicializa o estado de sessão para login
    if 'logado' not in st.session_state:
        st.session_state.logado = False
    if 'numero_da_conta' not in st.session_state:
        st.session_state.numero_da_conta = None
    
    menu = ["Possuo Conta", "Não possuo Conta", "Sair"]
    escolha = st.sidebar.selectbox("Menu", menu)
    
    # tem conta
    if escolha == "Possuo Conta":
        if not st.session_state.logado:
            numero_da_conta = st.number_input("Insira o número da conta", min_value=0, step=1)
            senha = st.text_input("Digite sua senha", type="password")
            
            # confirmação
            if st.button("Entrar"):
                senha_correta = verificar_senha(numero_da_conta=numero_da_conta)
                
                if senha == str(senha_correta):
                    st.session_state.logado = True
                    st.session_state.numero_da_conta = numero_da_conta
                    st.success(f"Click novamente")
                else:
                    st.error("Senha incorreta. Tente novamente.")
        else:
            numero_da_conta = st.session_state.numero_da_conta
            st.success(f"Bem-vindo, {exibir_nome(numero_da_conta)}")
            
            opcao_conta = st.selectbox("Escolha uma operação", ["Depositar", "Sacar", "Extrato", "Transferência", "Deletar Conta","Sair"])
            
            # depositar
            if opcao_conta == "Depositar":
                valor = st.number_input("Insira o valor que deseja depositar", min_value=0.0, step=0.01)
                
                if st.button("Confirmar Depósito"):
                    if valor > 0:
                        transacoes(numero_da_conta=numero_da_conta, valor=valor, tipo_de_transacao='deposito')
                        saldo = _salario(numero_da_conta=numero_da_conta)
                        ID = encontrar_id(numero_da_conta=numero_da_conta)
                        movimentacoes(saldo=saldo, tipo_de_operacao='D', tipo_de_conta='conta_corrente', id_cliente=ID)
                        st.success("Depósito realizado com sucesso.")
            
            # Sacar
            elif opcao_conta == "Sacar":
                valor = st.number_input("Insira o valor que deseja sacar", min_value=0.1, step=0.01)
                
                if st.button("Confirmar Saque"):
                    saldo_atual = _salario(numero_da_conta=numero_da_conta)
                    
                    if saldo_atual >= valor > 0:
                        transacoes(numero_da_conta=numero_da_conta, valor=valor, tipo_de_transacao='saque')
                        saldo = _salario(numero_da_conta=numero_da_conta)
                        ID = encontrar_id(numero_da_conta=numero_da_conta)
                        movimentacoes(saldo=saldo, tipo_de_operacao='S', tipo_de_conta='conta_corrente', id_cliente=ID)
                        st.success("Saque realizado com sucesso.")
                    else:
                        st.error("Saldo insuficiente.")
            
            # Extrato
            elif opcao_conta == "Extrato":
                st.text("Extrato: ")
                extrato(numero_da_conta=numero_da_conta)
                
            # Transferencia
            elif opcao_conta == "Transferência":
                numero_do_beneficiado = st.number_input("Insira o número da conta beneficiada", min_value=0, step=1)
                valor = st.number_input("Insira o valor que deseja transferir", min_value=0.0, step=0.01)
                
                if st.button("Confirmar Transferência"):
                    saldo_atual = _salario(numero_da_conta=numero_da_conta)
                    if saldo_atual >= valor > 0:
                        #A função retorna true se tudo estiver correto
                        if transferencia(valor=valor, numero_do_beneficiado=numero_do_beneficiado, numero_da_conta=numero_da_conta):
                            saldo = _salario(numero_da_conta=numero_da_conta)
                            ID = encontrar_id(numero_da_conta=numero_da_conta)
                            movimentacoes(saldo=saldo, tipo_de_operacao='T', tipo_de_conta='conta_corrente', id_cliente=ID)
                            
                        
                    else:
                        st.error("Saldo insuficiente.")
            
            # Apagar conta
            elif opcao_conta == "Deletar Conta":
                if st.button("Confirmar Exclusão"):
                    deletar(numero_da_conta=numero_da_conta)
                    st.success(f"Click novamente")
                    st.session_state.logado = False
                    st.session_state.numero_da_conta = None
            
            #Sair                    
            elif opcao_conta == "Sair":
                b = st.button('Encerrar sessão')
                if b:
                    st.success(f"Click novamente")
                    st.session_state.logado = False
                    st.session_state.numero_da_conta = None
                
    # Criar conta
    elif escolha == "Não possuo Conta":
        st.subheader("Crie sua conta")
        nome = st.text_input("Nome Completo")
        saldo_inicial = st.number_input("Depósito Inicial", min_value=0.0, step=0.01, placeholder='R$')
        senha = st.text_input("Senha", type="password")
        data =  str(datetime.now().date())
        tipo_de_conta = st.selectbox("Tipos de conta",["Conta corrente","Conta salário"])
        
        #tipo de conta
        if tipo_de_conta == "Conta corrente":
            tipo_de_conta='conta_corrente'
        elif tipo_de_conta == "Conta salário":
            tipo_de_conta = 'conta_salario'
        
        #confirmação
        if st.button("Criar Conta"):
            numero_da_conta = novo_numero()
            conexao = conexao_ao_banco()
            cursor = conexao.cursor()
            cursor.execute('INSERT INTO banco (numero_da_conta, nome, saldo, senha, _data_) VALUES (%s, %s, %s, %s,%s);', 
                           (numero_da_conta, nome, saldo_inicial, senha, data))
            
            conexao.commit()
            st.success(f"Conta criada com sucesso! Seu número de conta é {numero_da_conta}.")
            movimentacoes(id_cliente=encontrar_id(numero_da_conta=numero_da_conta),tipo_de_conta=tipo_de_conta,saldo=saldo_inicial, tipo_de_operacao="NC")
            conexao.close()           
    # Sair
    elif escolha == "Sair":
        st.session_state.logado = False
        st.session_state.numero_da_conta = None
        st.text("Obrigado por usar o sistema bancário.")

if __name__ == '__main__':
    load_dotenv()
    main()
