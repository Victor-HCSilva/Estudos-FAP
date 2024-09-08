from func_conexao_ao_banco import conexao_ao_banco
from random import randint

def novo_numero():
    try:
        
        conexao = conexao_ao_banco()
        cursor = conexao.cursor()
        
        if conexao:
            cursor.execute(
                '''SELECT numero_da_conta FROM banco; ''', 
            )
            lista_de_numeros = list(range(10000,100000,1) )#números possíveis de conta
            t = len(cursor.fetchall())#para garantir que não vá ocorrer um laço infinito
            
            #Se houver contas criadas
            if t > 0:
                while t:
                    numero = lista_de_numeros[randint(0,len(lista_de_numeros)-1)]
                    if numero not in cursor.fetchall():
                        return numero#retiornando um numero aleatório que não está contido na lista
                    t-=1
                    
            #Caso contrário o primeiro número retornado é 11111
            else:
                return 11111
        
            
    except Exception as erro:
        print(f'Erro na geração do número: {erro}')

##ok - retorna um número aletorio, que não está na lista de numeros no intervalo [10000,100000]
if __name__=='__main__':
    print(novo_numero())
   
        