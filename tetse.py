import pandas as pd


df2 = pd.DataFrame(
        {
           "A": 1.0,
           "B": pd.Timestamp("20130102"),
           "C": pd.Series(1, index=list(range(4)), dtype="float32"),
           
           "E": pd.Categorical(["test", "train", "test", "train"]),
           "F": "foo",
       }
   )

def es():
    nome = input('nome: ')
    numero = input('Numero: ')
    teste = input('Teste: ')
    
    df = pd.DataFrame(
        {
        'nome':[nome],
        'numero':[numero],
        'teste':[teste,]
        }
    )
    
    df.to_csv('out.csv', index=True)
    
    return 'Show'

def tt():
    nome = ('nome: ')
    numero = ('Numero: ')
    teste = ('Teste: ')
    
    df = pd.DataFrame(
        {
        'nome':[nome],
        'numero':[numero],
        'teste':[teste,]
        }
    )
    with open('out.csv',mode='a' ) as a:
        a.write(df)
    print('sho#2 tabelinhas, tabela de cadastro | movimentação, data, numero da conta, tipo de operação "Deposito",  "saque",  "conta criada ", "conta deletada"

#menu: cadastrar, deposito, saque, listar,apagar
#Novas contas , movimentações de contas 
#numero, nome, data, tipo, saldo  <<<------------ cadastro
#contas(lista de dicionários) -->> [{}]

#qual a conta a depositar? mostrar o id para ver se existe, se existir qual o valor para ser depositado
#Seguindo  (o saldo atual) - (o que foi depositado).
#saque --->> há limite de pedido (R$1000), verificar se há saque 
#Extrato -->> ver o saldo da conta

def cadastrar_conta(id, tipo ,nome, data,  saldo):
    try:
        user = [id,tipo, nome, data,  saldo]

        with open('teste.txt',mode='a', encoding='utf8') as dados:
            dados.write(str(user) )

        return print('Cadastrado!')
    
    except Exception as erro:
        return f'Erro ao salvar dados: {erro}'

def extrato(numero):

    with open('teste.txt', mode="r", encoding='utf8', newline='') as dados:
        dados = list(dados)
        print(dados)
    
    return None

def _movimentacao_(data, numero_conta, tipo_de_operacao):

    try:
        mov = [data, numero_conta, tipo_de_operacao]

        with open('mov_teste.txt',mode='a', encoding='utf8') as dados:
                dados.write(str(mov) )

        return '\nTudo ok'
    
    except Exception as erro:

        return f'Não foi possível salvar'

def sacar(numero_conta):
    try:
        quant = int(input('Digite o valor que quer sacar: '))

        if numero_conta:#verificar o saldo
            return quant-100

    except ValueError:
        return ('Inválido')

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
    try:
        movimentacao = True

        while movimentacao:
            
            operacao = escolha()
            
            if operacao == '1':

                novo_usuario = {
                    'tipo':'conta-corrente',#por enquanto
                    'numero': input("Insira o número"),#id
                    'nome':input("Insira seu nome: "),
                    'data' : input("Insira a data: "),
                    'saldo': 0,
                }
                
                cadastrar_conta(novo_usuario['numero'],novo_usuario['tipo'], novo_usuario['nome'], novo_usuario['data'], novo_usuario['saldo'])
            
            elif operacao == '2':
                print('2')
                pass#depositar()

            elif operacao == '3':
                numero_conta = input('Número: ')
                tipo_de_operacao = 'D'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                
                _movimentacao_(data, numero_conta, tipo_de_operacao)#salvando movimentação

                print('3')
                pass#sacar()

            elif operacao== '4':
                numero_conta = input('Número: ')
                tipo_de_operacao = 'E'#E = extrato, D=depositar,NC=nova conta,AC=apagar conta, S= sacar,
                

                _movimentacao_(data, numero_conta, tipo_de_operacao))#salvando movimentação

                extrato(numero_conta)

            elif operacao == '5':
                print('4')
                pass#apagar_conta()
            
            elif operacao== '6':
                movimentacao = False
 
    except Exception as erro:
        print(f'Erro ao realizar operação, à devs: {erro}')

    finally:
        print('Operação encerrada')

if __name__ =='__main__' :
    menu()

')
print(tt())