try:
    r=int(input(''))
    print(r/0)
except ValueError as erro:
    print(f"Erro: {type(erro).__name__}")