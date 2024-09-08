from func_conexao_ao_banco import conexao_ao_banco
from func_criar_nova_conta import criar_nova_conta
from func_verificar_conta import verificar_conta
from func_deletar import deletar
from func_extrato import extrato 
from func_id import encontrar_id
from func_transacoes import transacoes
from func_transferecia import transferencia
from func_saldo import _salario
from func_deletar import deletar
from func_movimentacoes import movimentacoes
from func_verificar_senha import verificar_senha

if __name__=='__main__':
    while True:
        print('\n1.Possuo conta')
        print('2.Não possuo conta')
        opcao = input('Digite a opção: ')
        
        if opcao == '1':
            conta = True
            
            numero_da_conta = int(input('\nInsira o numero da conta:'))#O número da conta é fornecido aqui
            senha = int(input('Digite sua senha: '))
            if senha == verificar_senha(numero_da_conta=numero_da_conta):
                print('\nOlá!')
                
                while conta:    
                    ID = encontrar_id(numero_da_conta=numero_da_conta)
                    print('0. Sair')
                    print('1. Depositar')
                    print('2. Sacar')
                    print('3. Extrato')
                    print('4. Transferência ')
                    print('5. deletar conta')
                    escolha = input('\nEscolha: ')
                    
                    #Depositar
                    if escolha == '1':
                        valor = float(input('\nInsira o valor que deseja depositar'))
                        
                        #se valor de deposito maoir que zero
                        if  valor > 0:
                            transacoes(numero_da_conta=numero_da_conta,valor=valor, tipo_de_transacao='deposito')
                            saldo = _salario(numero_da_conta=numero_da_conta)
                            movimentacoes(tipo_de_operacao='D', tipo_de_conta='conta_corrente',id=ID , saldo=saldo)
                        
                    #Sacar
                    elif escolha == '2':
                        valor = float(input('\nInsira o valor que deseja sacar'))
                        
                        #se valor menor ou igual ao saldo
                        if _salario(numero_da_conta=numero_da_conta) >= valor > 0:
                            transacoes(numero_da_conta=numero_da_conta,valor=valor, tipo_de_transacao='saque')
                            saldo = _salario(numero_da_conta=numero_da_conta)
                            movimentacoes(tipo_de_operacao='S', tipo_de_conta='conta_corrente',id=ID, saldo=saldo )
                        
                    # extrato
                    elif escolha == '3':
                        print('Extato: ')
                        extrato(numero_da_conta=numero_da_conta)
                    
                    #Tranferência contax -->> contay
                    elif escolha == '4':
                        print('\nTransferência')
                        numero_do_beneficiado = int(input('Insira o número da conta beneficiada: '))
                        valor = float(input('Insira o valor que deseja transferir'))
                        
                        if valor <= _salario(numero_da_conta):
                            transferencia(numero_da_conta=numero_da_conta,numero_do_beneficiado=numero_do_beneficiado,valor=valor)
                            id2 = encontrar_id(numero_do_beneficiado)
                            movimentacoes(tipo_de_operacao=f'{ID}->{id2}', tipo_de_conta='conta_corrente',id=ID, saldo=_salario(numero_da_conta) )
                            
                        else:
                            print('Saldo insuficiente.')
                             
                    elif escolha == '5':
                        while True:
                            print('\nDeletar conta: ')
                            print('1. Deletar conta permanentemente')
                            print('0. Cancelar')
                            escolha_ = input('Digite (1 ou 0)): ')
                            
                            if escolha_ == '1':
                                senha = int(input('Insira a senha para confirmar'))
                                if verificar_senha(numero_da_conta=numero_da_conta):
                                    deletar(numero_da_conta=numero_da_conta)
                                    break
                            elif escolha_ == '0':
                                break
                            
                    elif escolha == '0':
                        conta = False
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
            else:
                print('\nSenha ou número da conta estão incorretos, repita a operação.')
            
        #Criar uma conta    
        elif opcao == '2':
            print('\nPor padrão você receberá um número que irá corresponder a sua conta, seu saldo será R$0. ')
            nome = input('Insira nome: ').title()
            saldo = 0
            
            while True:
                print('\n1.Conta corrente\n2. Conta salário')
                s = input('digite (1 ou 2): ')
                
                if s =='1':
                    tipo_de_conta = 'conta_corrente'
                    break
                elif s =='2':
                    tipo_de_conta = 'conta_salario'
                    break
                
            #Execução das funções
            criar_nova_conta(nome=nome, saldo=saldo)
            numero_da_conta = int(input('Finalize digitando seu número da conta: '))
            ID = encontrar_id(numero_da_conta=numero_da_conta)
            movimentacoes(tipo_de_operacao='NC', tipo_de_conta='conta_corrente',id=ID, saldo=saldo )
            print('\nGuarde seu número e senha.')
            
        elif opcao == '0':
            break
            
            