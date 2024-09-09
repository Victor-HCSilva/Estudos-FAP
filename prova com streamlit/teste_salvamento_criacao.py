st.subheader("Crie sua conta")
        nome = st.text_input("Nome Completo")
        saldo_inicial = st.number_input("Depósito Inicial", min_value=0.0, step=0.01)
        senha = st.text_input("Senha", type="password")
        data =  str(datetime.now().date())
        tipo_de_conta = st.selectbox(["Conta corrente","Conta salário"])
        
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
            cursor.execute('INSERT INTO banco (numero_da_conta, nome, saldo, senha, _data_) VALUES (%s, %s, %s, %s);', 
                           (numero_da_conta, nome, saldo_inicial, senha, data))
            
            conexao.commit()
            st.success(f"Conta criada com sucesso! Seu número de conta é {numero_da_conta}.")
            
            movimentacoes(id_cliente=encontrar_id(numero_da_conta=numero_da_conta),tipo_de_conta=tipo_de_conta,saldo=saldo_atual, tipo_de_operacao="NC")
            
            