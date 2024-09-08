#2 tabelinhas, tabela de cadastro | movimentação, data, numero da conta, tipo de operação "Deposito",  "saque",  "conta criada ", "conta deletada"

#menu: cadastrar, deposito, saque, listar,apagar
#Novas contas , movimentações de contas 
#numero, nome, data, tipo, saldo  <<<------------ cadastro
#contas(lista de dicionários) -->> [{}]

#qual a conta a depositar? mostrar o id para ver se existe, se existir qual o valor para ser depositado
#Seguindo  (o saldo atual) - (o que foi depositado).
#saque --->> há limite de pedido (R$1000), verificar se há saque 
#Extrato -->> ver o saldo da conta



'''
PARA VOCÊ (2024-08-23)!!!!

consertar a pesquisa de todos para que possam retornar tudo corretamente, 
não está nada sendo salvo. é possível colocar as operações em menos funções
apenas dependendo do tipo de operação[deixaria o código mais compacto], ademais 
as funcionalidades estão funcionando bém. Falta: deleção, tipos de conta, tratamnetos 
de erro, e salvamento de dados e operações [vide a nomeclatura adotada para tal].
E pode adicionar o que quiser a mais para ter o bonus do plus+++

'''




def _movimentacao_(data, numero_conta, tipo_de_operacao):

    try:
        mov = [data, numero_conta, tipo_de_operacao]

        with open('mov_teste.txt',mode='a', encoding='utf8', newline='\n') as dados:
                dados.write(str(mov) )

        return '\nTudo ok'
    
    except Exception as erro:

        return f'Não foi possível salvar'

def cadastrar_conta(id, tipo ,nome, data,  saldo):
    try:
        user = [id,tipo, nome, data,  saldo]

        with open('teste.txt',mode='a', encoding='utf8') as dados:
            dados.write(str(user) )

        return print('Cadastrado!')
    
    except Exception as erro:
        return f'Erro ao salvar dados: {erro}'

    
def escolha():
    while True:
        print('\n1.Cadastrar nova conta.')
        print('2.Depositar. ')
        print('3.Sacar.')
        print('4.Extrato')
        print('5.Apagar conta.')
        print('6.Cancelar. ')
        operacao = input('O que deseja fazer? ')

        if operacao == '1' or operacao == '2' or operacao == '3' or operacao == '4' or operacao == '5' or operacao == '6':
            return operacao
        
        else:
            print('Opção inválida')

def menu():
    data = '2024-08-23'#data que será salva nas movimentações
    cadastro=[]
    try:
        movimentacao = True

        while movimentacao:
            
            operacao = escolha()
            
            if operacao == '1':

                novo_usuario = {
                    'tipo':'conta-corrente',#por enquanto
                    'numero': int(input("Insira o número")),#id
                    'nome':input("Insira seu nome: "),
                    'data' : input("Insira a data (YYYY-MM-DD): "),
                    'saldo': 0,
                }
                
                '''novo_usuario2 = {
                    'tipo':'conta-corrente',#por enquanto
                    'numero': 2,#input("Insira o número"),#id
                    'nome':'Teste da silva ',#input("Insira seu nome: "),
                    'data' :'2024-08-23',# input("Insira a data: "),
                    'saldo': 0,
                }
                '''
                cadastrar_conta(novo_usuario['numero'],novo_usuario['tipo'], novo_usuario['nome'], novo_usuario['data'], novo_usuario['saldo'])
                '''cadastrar_conta(novo_usuario2['numero'],novo_usuario2['tipo'], novo_usuario2['nome'], novo_usuario2['data'], novo_usuario2['saldo'])'''
                cadastro.append(novo_usuario)#add novo usuario
                '''cadastro.append(novo_usuario2)#add novo usuario'''
                tipo_de_operacao='NC'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                
            #depositar
            
            elif operacao == '2':
                #parâmetros(numero_conta,dados, deposito)
                
                if cadastro:
                    print('Oi no 2')
                    numero_conta = int(input('numero da conta: '))
                    deposito = float(input('Insira o valor que deseja depositar:'))
                    dados = cadastro   
                    tipo_de_operacao='D'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                    
                    _movimentacao_(data, numero_conta, tipo_de_operacao)   
                     
                    for s in range(len(dados)):
                        print(f'Comparações: {dados[s]['numero']} e {numero_conta}')
                        
                        if dados[s]['numero'] == numero_conta:
                            dados[s]['saldo']+=deposito
                            
                            print(f'Saldo atual: {dados[s]['saldo']}')
                            msg='Encontrado!'
                            break
                        else:
                            msg='Não encontrado'
                            
                    print(msg)                    
    
            #sacar
            elif operacao == '3':
                if cadastro:
                    tipo_de_operacao='S'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                    numero_conta = int(input('Número: '))
                    tipo_de_operacao = 'D'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                    saque_quantidade = float(input('Valor que deseja sacar: '))
                    dados = cadastro
                    _movimentacao_(data, numero_conta, tipo_de_operacao)
                    for s in range(len(dados)):
                        print(f'Comparações: {dados[s]['numero']} e {numero_conta}')
                        
                        if dados[s]['numero'] == numero_conta:
                            msg=('Encontrado')
                            
                            if (dados[s]['saldo']- saque_quantidade) >= 0:
                                dados[s]['saldo']-= saque_quantidade
                                print(f'Saldo atual: {dados[s]['saldo']}')
                                break
                            else:
                                msg='Encontrado, pórem a ação não pode ser feita'
                                print('Não é possível realizar a operação')
                                break
                        else:
                            msg ='Não encontrado'
                            
                    print(msg)
                else:
                    print('Não há nenhum registro')

            #Extrato
            elif operacao== '4':
                
                if  cadastro:
                    tipo_de_operacao='E'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                    numero_conta = int(input('Número: '))
                    tipo_de_operacao = 'E'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar
                    dados = cadastro
                    _movimentacao_(data, numero_conta, tipo_de_operacao)
                    
                    for s in range(len(dados)):
                        print(f'Comparações: {dados[s]['numero']} e {numero_conta}')
                        
                        if dados[s]['numero'] == numero_conta:
                            print(dados[s])
                            msg='Encontrado!'
                            break
                        else:
                            msg='Não encontrado'
                            
                    print(msg)  
                                     
                else:
                    print('Não há nenhum registro')
                    
            #apagar conta
            elif operacao == '5':
        
                if cadastro:
                    numero_conta = int(input('Número: '))
                    dados = cadastro
                    tipo_de_operacao = 'AC'
                    _movimentacao_(data, numero_conta, tipo_de_operacao)
                    
                    for s in range(len(dados)):
                        print(f'Comparações: {dados[s]['numero']} e {numero_conta}')
                        
                        if dados[s]['numero'] == numero_conta:
                            msg='Deletado!'
                            dados.remove(dados[s])
                            break
                        else:
                            msg='Não encontrado'
                            
                    print(msg)  
                                     
                else:
                    print('Ainda não há nenhum registro')
                    
            elif operacao== '6':
                movimentacao = False
 
    except Exception as erro:
        print(f'Erro ao realizar operação, à devs: {erro}')

    finally:
        print('Operação encerrada')

if __name__ =='__main__' :
    menu()

