def _senha():
    
        while True:
            try:
                senha = input('\n\ncrie uma senha para sempre acessar sua conta, deve conter:\n1.4 digitos\n2.Apenas números inteiros ')
                if len(senha) >= 4:
                    return int(senha)
                else:
                    print('4 digitos são necessários')    
            except:
                print('\nPor favor, apenas numeros inteiros.')
        
if __name__=='__main__':
    print(_senha())