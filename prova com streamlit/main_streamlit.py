from _funcoes_ import *
from func_saldo import _salario

with open('estilo.css') as estilo:
    st.markdown(f'<style>{estilo.read()}</style>',unsafe_allow_html=True)

load_dotenv()
def main():
    try:
        st.title("Sistema Bancário simples 💸")
        # Inicializa o estado de sessão para login
        if 'logado' not in st.session_state:
            st.session_state.logado = False
        if 'numero_da_conta' not in st.session_state:
            st.session_state.numero_da_conta = None
        
        menu = ["login", "Criar conta", "Sair"]
        escolha = st.sidebar.selectbox("Menu", menu, index= 1 )
        
        # tem conta
        if escolha == "login":
            if not st.session_state.logado:
                st.subheader('Login')
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
                    valor = st.number_input("Insira o valor que deseja depositar R$", min_value=0.0, step=0.01, placeholder='R$')
                    
                    if st.button("Confirmar Depósito"):
                        if valor > 0:
                            transacoes(numero_da_conta=numero_da_conta, valor=valor, tipo_de_transacao='deposito')
                            saldo = _salario(numero_da_conta=numero_da_conta)
                            ID = encontrar_id(numero_da_conta=numero_da_conta)
                            movimentacoes(saldo=saldo, tipo_de_operacao='D', tipo_de_conta='conta_corrente', id_cliente=ID)
                            st.success("Depósito realizado com sucesso.")
                
                # Sacar
                elif opcao_conta == "Sacar":
                    valor = st.number_input("Insira o valor que deseja sacar R$", min_value=0.1, step=0.01, placeholder='R$')
                    
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
        elif escolha == "Criar conta":
            st.subheader("Crie sua conta")
            nome = st.text_input("Nome Completo", placeholder='Insira seu nome')
            saldo_inicial = st.number_input("Depósito Inicial", min_value=0.0, step=0.01, placeholder='R$')
            senha = st.text_input("Senha", type="password", placeholder='Apenas numeros inteiros')
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
            os.system('exit()')
    except:
        pass
        st.error('por favor verifique se tudo foi preenchido corretamente', icon="🚨",)
        
if __name__ == '__main__':
    load_dotenv()
    main()
