from class_banco import *
#Menu
while True:
    banco = Banco()
    try:
        DATA = str(datetime.now())
        MOVIMENTCOES = []
        print('\n1. Criar nova conta.')
        print('2. Depositar.')
        print('3. Sacar.')
        print('4. Extrato.')
        print('5. Apagar conta.')
        print('6. Alterar nome.')
        print('7. Transferência.')
        print('0. Cancelar.')

        opcao = input('Digite a opção escolhida: ')

        # Criar conta
        if opcao == '1':
            nome = input('Nome: ').title()
            numero_da_conta = int(input('Número da conta: '))

            while True:
                tipo_de_conta = input('Tipo de conta: 1-conta corrente 2-conta poupança: ')
                if tipo_de_conta == '1':
                    tipo_de_conta = 'conta_corrente'
                    break
                elif tipo_de_conta == '2':
                    tipo_de_conta = 'conta_poupanca'
                    break
            saldo = 0

            if banco.verificar_conta(numero_da_conta=numero_da_conta, nome=nome):
                print('Já existe uma conta com este número, por favor tente outro.')
            else:
                banco.criar_conta(data=str(DATA), nome=nome, numero_da_conta=numero_da_conta, tipo_de_conta=tipo_de_conta, saldo=saldo)

        # Depositar/sacar
        elif opcao == '2':
            valor = float(input('Valor que deseja depositar: '))
            numero_da_conta = int(input('Número da conta: '))
            nome = input(f"Insira o nome do titular da conta {numero_da_conta}: ")
            tipo_de_operacao = 'D'

            if valor > 0:
                if banco.verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                    banco.realizar_transacao(numero_da_conta=numero_da_conta, valor=valor, tipo_transacao=1)
                    banco.salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao, data=DATA,  saldo=banco._saldo(numero_da_conta))
                else:
                    print('\nErro na transação.')
            else:
                print('\nInválido valor menor ou igual a zero.')
            
                    # Depositar/sacar
        elif opcao == '2':
       
            valor = float(input('Valor que deseja depositar: '))
            if valor <= 0:
                print('\nInválido: valor menor ou igual a zero.')
            else:
                numero_da_conta = int(input('Número da conta: '))
                nome = input(f"Insira o nome do titular da conta {numero_da_conta}: ")
                tipo_de_operacao = 'D'  # D para depósito

                if banco.verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                    # Realiza a transação
                    banco.realizar_transacao(numero_da_conta=numero_da_conta, valor=valor, opcao=1)

                    # Salva a movimentação
                    banco.salvar_movimentacoes(id=banco.encontrar_id(numero_da_conta=numero_da_conta), tipo_de_operacao='D', data=DATA, saldo=banco._saldo(numero_da_conta))
                    print('\nDepósito realizado com sucesso!')
                    
                else:
                    print('\nErro na transação: Conta não encontrada.')
       
             
           # Sacar
        elif opcao == '3':
            valor = float(input('Valor que deseja sacar: '))
            numero_da_conta = int(input('Número da conta: '))
            nome = input(f"Insira o nome do titular da conta {numero_da_conta}: ")
            tipo_de_operacao = 'S'

            if valor > 0:
                if banco.verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                    banco.realizar_transacao(numero_da_conta=numero_da_conta, valor=valor, tipo_transacao=2)
                    banco.salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao, data=DATA,  saldo=banco._saldo(numero_da_conta))
                else:
                    print('\nErro na transação.')
            else:
                print('\nInválido valor menor ou igual a zero.')
                
    
            
#a partir daqui é necessario aplicar todo a classe Banco e ver como se comportam os métodos
# A class Banco está em class_banco.py
# _mais_funções_.py comporta algumas funções no fim do seu código que podem ser úteis
# prova_V3 apresenta total funcionamento, dentro do que ele propõem, e não têm nada a ver com
# os métodos da class banco. Estes são os condigos mais relevantes.
# 
# 
# 
# ______________________________________________________________________________________________________________________________________________________________________    
   
        # Extrato
        elif opcao == '4':
            numero_da_conta = int(input('\nInsira o número da conta: '))
            nome = input('Insira o nome: ')
            if banco.verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                banco.extrato(numero_da_conta=numero_da_conta,nome=nome)
                

        # Excluir conta
        elif opcao == '5':
            numero_da_conta = int(input('\nNúmero da conta: '))
            nome = input('Nome do titular da conta: ').title()
            
            if banco.verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
                banco.deletar(numero_da_conta, nome)
            else:
                print('\nNão encontrado, verifique se tudo foi digitado corretamente.')
                
    


        # Mudanças de nome ou número de conta
        elif opcao == '6':
            nome = input('Insira o nome antigo: ').title()
            novo_nome = input('Insira o novo nome: ')
            numero_da_conta = input('Insira o Número da conta: ')
            if banco.verificar_conta(nome=nome, numero_da_conta=numero_da_conta):
               banco.mudar_nome(numero_da_conta=numero_da_conta, novo_nome=novo_nome)

            
        # Transferência
        elif opcao == "7":
            numero_da_conta = int(input('Insira o número da conta do transferidor: '))
            nome = input('Nome do tranferidor: ')
            numero_do_beneficiado = int(input('Insira o número da conta do beneficiário: '))
            valor = int(input('Insira o valor da transferência: '))

            if 0 < valor <= banco._saldo(numero_da_conta=numero_da_conta):
                banco.transferencia(numero_da_conta=numero_da_conta, numero_do_beneficiado=numero_do_beneficiado, valor=valor)
                banco.salvar_movimentacoes(data=DATA, tipo_de_operacao="T",  saldo=banco._saldo(numero_da_conta=numero_da_conta), )
            else:
                print('\nAção não possivel')
                    
    except Exception as e:
            print(e)
            
##Não ta salvando em movimentações            
'''     # Sair
        elif opcao == '0':
            print('Programa encerrado')
            break   

    except ValueError as e:
        print('\nVocê digitou algo incorreto, por favor repetir ação.')
        
    except Exception:
        print(f'\nOps aconteceu um imprevisto: {Exception}')
'''