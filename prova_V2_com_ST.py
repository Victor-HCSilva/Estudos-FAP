from datetime import datetime
from _funcoes_ import mostrar_id  # Certifique-se de que este arquivo exista e tenha a função mostrar_id
import mysql.connector
import streamlit as st

def conexao_ao_banco():
    tabelas = '''
        create database BANCO_PROVA_FAP_v3;
        use BANCO_PROVA_FAP_v3;
        
        create table if not exists banco (
            id_cliente INT AUTO_INCREMENT ,
            numero_da_conta int not null,
            nome varchar(100) not null,
            tipo_de_conta text not null,
            _data_ date not null,
            saldo decimal(65,2) not null ,
            PRIMARY KEY(id_cliente)
        );
        create table if not exists movimentacoes (
                id_cliente INT not null,
                tipo_de_operacao varchar(2) not null,
                _data_ date not null,
                saldo decimal(65,2) not null
                );
        '''

    
    try:
        conexao = mysql.connector.connect(
                host='localhost',
                database='BANCO_PROVA_FAP_v3',
                user='root',
                password='V1ct0r_Hug@'
            )
    
        return conexao
        
    except Exception as erro:
        print(f'Erro ao conectar ao banco de dados: {erro}')
        st.error(f"Erro ao conectar ao banco de dados: {erro}")
        return None

def mudanca(nome=None,numero_da_conta=None,id=None, tipo_de_alteracao=None):
    try:
        conexao = conexao_ao_banco()
            
        if conexao.is_connected():
            #criar uma conta
            
            if tipo_de_alteracao == '1':
                cursor = conexao.cursor()
                user = """UPDATE banco SET nome = %s WHERE (numero_da_conta =%s);
                                    """
                                    #(tipo_de_conta ,nome, data,  saldo, numero_da_conta)
                cursor.execute(user, (nome,numero_da_conta))
                conexao.commit()
                        
                print('\nMudança de nome realizada!')
                st.success("Mudança de nome realizada!")
                
            elif tipo_de_alteracao == '2':
                cursor = conexao.cursor()
                user = """UPDATE banco SET numero_da_conta = %s WHERE (id_cliente =%s);"""
                                    
                cursor.execute(user, (numero_da_conta,id))
                conexao.commit()
                print('\nMudança de número realizada!')
                st.success("Mudança de número realizada!")
                
    except Exception as erro:
        print(f'Erro: {erro}')
        st.error(f"Erro: {erro}")
            
    finally:
        if conexao.is_connected:
            conexao.close()



def extrato(id):
    conexao = None
    try:
        # Conexão com o banco de dados
        conexao = conexao_ao_banco()
        
        if conexao.is_connected():
            
            if conexao.is_connected():
            #criar uma conta
            
                    
                cursor = conexao.cursor()
                user = 'select * from banco where id_cliente = %s;'
                
                cursor.execute(user, (id,))
                saldo = cursor.fetchall()[0][5]
                if saldo:
                    print('Saldo:',saldo)
                    st.write(f"Saldo: {saldo}")
                    
                cursor = conexao.cursor()
                user = 'select * from movimentacoes where id_cliente = %s;'
                
                cursor.execute(user, (id,))
                
                for s in cursor.fetchall():
                    print(s)
                    st.write(s)
            
        else:
            print('Não foi possível conectar ao banco de dados.')
            st.error("Não foi possível conectar ao banco de dados.")

    except Exception as erro:
        print(f"Erro ao buscar extrato: {erro}")
        st.error(f"Erro ao buscar extrato: {erro}")

    finally:
        if conexao and conexao.is_connected():
            conexao.close()

def criar_conta(data,nome,numero_da_conta,tipo_de_conta, saldo):
    try:
        conexao = conexao_ao_banco()
            
        if conexao.is_connected():
            #criar uma conta
            
                    
            cursor = conexao.cursor()
            user = """INSERT INTO banco (numero_da_conta, nome, tipo_de_conta,_data_, saldo)
                                VALUES (%s, %s, %s, %s,%s )"""
                                #(tipo_de_conta ,nome, data,  saldo, numero_da_conta)
            user_dados = (numero_da_conta, nome, tipo_de_conta, data, saldo)
            cursor.execute(user, user_dados)
            conexao.commit()
                    
            print('\ncadastrado!')
            st.success("Conta criada com sucesso!")
                    
    except Exception as erro:
        print(f'Erro na inserção dos dados: {erro}')
        st.error(f"Erro na inserção dos dados: {erro}")
            
    finally:
        if conexao.is_connected:
            conexao.close()
    
def depositar(numero_da_conta, valor):
    try:
        # Convertendo o valor para o tipo correto
        valor = float(valor)

        # Conexão com o banco de dados
        conexao = conexao_ao_banco()

        # Usando with para garantir o fechamento do cursor
        with conexao.cursor() as cursor:
            # Atualizando o saldo
            atualizar_saldo = 'UPDATE banco SET saldo = saldo + %s WHERE numero_da_conta = %s;'
            cursor.execute(atualizar_saldo, (valor, numero_da_conta))
            conexao.commit()

            # Verificando o novo saldo
            consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
            cursor.execute(consulta_saldo, (numero_da_conta,))
            resultado = cursor.fetchone()

            if resultado:
                novo_saldo = resultado[0]
                print(f'Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}')
                st.success(f"Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}")
            else:
                print('Número da conta não encontrado.')
                st.error("Número da conta não encontrado.")

    except Exception as erro:
        print(f"Erro ao depositar: {erro}")
        st.error(f"Erro ao depositar: {erro}")

    finally:
        if conexao.is_connected():
            conexao.close()

def sacar(numero_da_conta, valor):
    try:
        # Convertendo o valor para o tipo correto
        valor = float(valor)

        # Conexão com o banco de dados
        conexao = conexao_ao_banco()

        # Usando with para garantir o fechamento do cursor
        with conexao.cursor() as cursor:
            # Atualizando o saldo
            atualizar_saldo = 'UPDATE banco SET saldo = saldo - %s WHERE numero_da_conta = %s;'
            cursor.execute(atualizar_saldo, (valor, numero_da_conta))
            conexao.commit()

            # Verificando o novo saldo
            consulta_saldo = 'SELECT saldo FROM banco WHERE numero_da_conta = %s;'
            cursor.execute(consulta_saldo, (numero_da_conta,))
            resultado = cursor.fetchone()

            if resultado:
                novo_saldo = resultado[0]
                print(f'Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}')
                st.success(f"Saldo atualizado com sucesso. Saldo atual: {novo_saldo:.2f}")
            else:
                print('Número da conta não encontrado.')
                st.error("Número da conta não encontrado.")

    except Exception as erro:
        print(f"Erro ao sacar: {erro}")
        st.error(f"Erro ao sacar: {erro}")

    finally:
        if conexao.is_connected():
            conexao.close()

def deletar(numero_da_conta, nome):
    try:
        conexao = conexao_ao_banco()
        cursor=conexao.cursor()
        executar = 'DELETE FROM banco WHERE numero_da_conta = %s and nome = %s;'
            
        cursor.execute(executar, (numero_da_conta,nome))  
        conexao.commit() 
        
        print('Conta encerrada')
        st.success("Conta encerrada com sucesso!")
           
    except Exception as erro:
        print(f"Erro ao tentar excluir permanentemente a conta: {erro}")
        st.error(f"Erro ao tentar excluir permanentemente a conta: {erro}")
            
    finally:
        if conexao.is_connected():
            conexao.close()

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
        st.success("Movimentação salva com sucesso!")
        
    except Exception as erro:
        print(f'\nErro ao mostrar histórico de movimentações: {erro}')
        st.error(f"Erro ao mostrar histórico de movimentações: {erro}")
        
    finally:
        if conexao.is_connected():
            conexao.close()

def main():
    st.title("Banco Simples")

    while True:
        DATA = str(datetime.now())
        MOVIMENTCOES = []
        st.sidebar.title("Menu")
        opcao = st.sidebar.selectbox(
            'Escolha uma opção:',
            ['Criar nova conta', 'Depositar', 'Sacar', 'Extrato', 'Apagar conta', 'Realizar mudanças', 'Cancelar']
        )

        if opcao == 'Criar nova conta':
            nome = st.sidebar.text_input("Nome: ").title()
            numero_da_conta = st.sidebar.number_input("Número da conta:", value=0, min_value=0, step=1)
            tipo_de_conta = st.sidebar.selectbox('Tipo de conta:', ['conta_corrente', 'conta_poupanca'])
            saldo = 0
            criar_conta(data=DATA, nome=nome, numero_da_conta=numero_da_conta, tipo_de_conta=tipo_de_conta, saldo=saldo)

        elif opcao == 'Depositar':
            valor = st.sidebar.number_input("Valor desejado:", value=0, min_value=0, step=0.01)
            numero_da_conta = st.sidebar.number_input("Número da conta:", value=0, min_value=0, step=1)
            tipo_de_operacao = 'D'
            depositar(numero_da_conta, valor)
            salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao, _data_=DATA, id=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'), saldo=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'))

        elif opcao == 'Sacar':
            valor = st.sidebar.number_input("Valor desejado:", value=0, min_value=0, step=0.01)
            numero_da_conta = st.sidebar.number_input("Número da conta:", value=0, min_value=0, step=1)
            saldo = 0  # 'verificar saldo'
            tipo_de_operacao = 'S'
            sacar(numero_da_conta=numero_da_conta, valor=valor)
            salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao, _data_=DATA, id=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'), saldo=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'))

        elif opcao == 'Extrato':
            numero_da_conta = st.sidebar.number_input("Número da conta:", value=0, min_value=0, step=1)
            extrato(id=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'))

        elif opcao == 'Apagar conta':
            numero_da_conta = st.sidebar.number_input("Número da conta:", value=0, min_value=0, step=1)
            nome = st.sidebar.text_input("Nome do titular da conta:")
            deletar(numero_da_conta, nome)

        elif opcao == 'Realizar mudanças':
            escolha = st.sidebar.selectbox(
                'O que deseja mudar?',
                ['Mudar nome', 'Número da conta']
            )

            if escolha == 'Mudar nome':
                nome = st.sidebar.text_input("Novo nome:")
                numero_da_conta = st.sidebar.number_input("Número da conta:", value=0, min_value=0, step=1)
                mudanca(nome=nome, numero_da_conta=numero_da_conta, tipo_de_alteracao=escolha)

            elif escolha == 'Número da conta':
                numero_da_conta = st.sidebar.number_input("Novo número da conta:", value=0, min_value=0, step=1)
                id = st.sidebar.text_input("ID do cliente:")
                mudanca(id=id, numero_da_conta=numero_da_conta, tipo_de_alteracao=escolha)

        elif opcao == 'Cancelar':
            break

if __name__ == '__main__':
    import streamlit as st
from datetime import datetime
from _funcoes_ import mostrar_id
import mysql.connector

# Funções do banco de dados aqui (copie e cole suas funções, como `conexao_ao_banco`, `criar_conta`, etc.)

st.title("Sistema Bancário")

# Seções para escolher a operação
opcao = st.selectbox('Escolha a operação:', ['Criar nova conta', 'Depositar', 'Sacar', 'Extrato', 'Apagar conta', 'Realizar mudanças'])

if opcao == 'Criar nova conta':
    nome = st.text_input('Nome:')
    numero_da_conta = st.number_input('Número da conta:', min_value=1)
    tipo_de_conta = st.selectbox('Tipo de conta:', ['conta_corrente', 'conta_poupanca'])
    saldo = st.number_input('Saldo inicial:', min_value=0.0, value=0.0)
    
    if st.button('Criar Conta'):
        DATA = str(datetime.now())
        criar_conta(data=DATA, nome=nome, numero_da_conta=numero_da_conta, tipo_de_conta=tipo_de_conta, saldo=saldo)
        st.success(f'Conta criada para {nome} com sucesso!')

elif opcao == 'Depositar':
    numero_da_conta = st.number_input('Número da conta:', min_value=1)
    valor = st.number_input('Valor do depósito:', min_value=0.0)
    
    if st.button('Depositar'):
        depositar(numero_da_conta, valor)
        st.success(f'Depósito de {valor} realizado com sucesso!')

elif opcao == 'Sacar':
    numero_da_conta = st.number_input('Número da conta:', min_value=1)
    valor = st.number_input('Valor do saque:', min_value=0.0)
    
    if st.button('Sacar'):
        sacar(numero_da_conta, valor)
        st.success(f'Saque de {valor} realizado com sucesso!')

elif opcao == 'Extrato':
    numero_da_conta = st.number_input('Número da conta:', min_value=1)
    
    if st.button('Mostrar Extrato'):
        saldo = extrato(id=mostrar_id(numero_da_conta=numero_da_conta, opcao='2'))
        st.write(f'Saldo atual: {saldo}')

elif opcao == 'Apagar conta':
    numero_da_conta = st.number_input('Número da conta:', min_value=1)
    nome = st.text_input('Nome do titular:')
    
    if st.button('Apagar Conta'):
        deletar(numero_da_conta, nome)
        st.success(f'Conta apagada com sucesso!')

elif opcao == 'Realizar mudanças':
    tipo_mudanca = st.selectbox('Escolha a mudança:', ['Mudar nome', 'Mudar número da conta'])
    
    if tipo_mudanca == 'Mudar nome':
        nome = st.text_input('Novo nome:')
        numero_da_conta = st.number_input('Número da conta:', min_value=1)
        if st.button('Atualizar Nome'):
            mudanca(nome=nome, numero_da_conta=numero_da_conta, tipo_de_alteracao='1')
            st.success('Nome atualizado com sucesso!')
    
    elif tipo_mudanca == 'Mudar número da conta':
        id_cliente = st.number_input('ID do cliente:', min_value=1)
        novo_numero = st.number_input('Novo número da conta:', min_value=1)
        if st.button('Atualizar Número da Conta'):
            mudanca(id=id_cliente, numero_da_conta=novo_numero, tipo_de_alteracao='2')
            st.success('Número da conta atualizado com sucesso!')
