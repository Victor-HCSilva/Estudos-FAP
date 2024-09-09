
import os
from pathlib import Path
from random import randint
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

# Defina o caminho completo para o arquivo .env
caminho_env = Path('C:/Users/victo/Desktop/.env')  # Usando barras normais ou duplas barras invertidas
load_dotenv(dotenv_path=caminho_env)

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

'''


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



'''