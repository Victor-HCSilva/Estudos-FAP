from _funcoes_ import deletar,extrato,mostrar_id,conexao_ao_banco,depositar,salvar_movimentacoes,escolha
from datetime import datetime
import  mysql.connector
from _funcoes_ import _Banco_

#ok
def criar_conta():
    banco = _Banco_()
    
    while True:
        DATA = str(datetime.now())
        TIPO_DE_CONTA = ('conta_corrente','conta_salario','conta_poupanca', 'conta_pagamento')
        
        try:
            while True:
                print('\nTipo de conta:\n1.conta corrente\n2.conta salário\n3.conta poupança\n4.conta pagamento')
                tipo = int(input('Escolha: '))
                
                tipo_de_conta = TIPO_DE_CONTA[tipo-1]
                            
                if 0 < tipo < 5:                    
                    break
                
                print(f'Escolha Inválida: {tipo}')
                
            break    
        
        except ValueError:        
            print(f'\nValor inválido.')
    try:
        numero_da_conta = float(input('Número da conta: '))
        nome = input('Insira o nome: ').title()
        saldo = 0    
        tipo_de_operacao='NC'

        banco.novo_usuario(nome=nome,data=DATA,saldo=saldo,numero_da_conta=numero_da_conta,tipo_de_conta=tipo_de_conta)
        salvar_movimentacoes(tipo_de_operacao=tipo_de_operacao,_data_=DATA,saldo=0, id=mostrar_id(opcao=1,numero_da_conta=numero_da_conta))
        
    except ValueError:
        print('Valor inválido')
        
    except Exception as erro:
        print(f'Erro: {erro}')
        
    finally:
        print('Fim da operação')
        
        
        
def _extrato_():
    data = str(datetime.now())
    banco = _Banco_()
    numero = input('Insira o número da conta: ')
    banco.extrato(id=mostrar_id(opcao=1,numero_da_conta=numero))
    salvar_movimentacoes(tipo_de_operacao='D',_data_=data,id=mostrar_id(opcao=1,numero_da_conta=numero))
    
    
'''
        
        print('\n1.Criar nova conta.')
        print('2.Depositar. ')
        print('3.Sacar.')
        print('4.Extrato')
        print('5.Apagar conta.')
        print('0.Cancelar. ')
        operacao = input('O que deseja fazer? ')
        
        '''
#ok        
def depositar_valor():
    data = str(datetime.now())
    banco = _Banco_()   
    while True:
        try:
            numero = int(input('Número: '))
            valor = float(input('Insira o valor a ser depositado: '))
            break
            
        except ValueError:
            print('Inválido')
            
    banco.depositar(id=mostrar_id(opcao=1,numero_da_conta=numero),valor=valor)
    id = mostrar_id(opcao=1,numero_da_conta=numero)
    saldo = mostrar_id(opcao=2,numero_da_conta=numero)
    salvar_movimentacoes(tipo_de_operacao='D',_data_=data,id=id, saldo=saldo)
    
def deletar_conta():
    banco = _Banco_
    
    while True:
        
        try:
            numero=int(input('Insira o número da conta'))
            break
        
        except ValueError as erro:
            print(f'Erro: {erro}')
    
    try:    
        banco.deletar(id=mostrar_id(numero_da_conta=numero,opcao='1'))
        
    except Exception as erro:
        print(f'Erro ao tentar apagar conta: {erro}')

def _menu_():
    menu = True
    while menu: 
        _escolha_ = escolha()
        
        if _escolha_ == '1':#Criar conta
            criar_conta()
        elif _escolha_ == '2':#Depositar valor
            depositar_valor()
        elif _escolha_ == '3':#Sacar
            pass
        elif _escolha_ == '4':#Extrato
            _extrato_()
        
        elif _escolha_ == '5':#Deletar
            deletar_conta()
        elif _escolha_ == '0':#Sair:
            menu=False
            
if __name__=='__main__':
    _menu_()