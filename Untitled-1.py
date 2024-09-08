import csv

dados = [
      ['Nome', 'Idade', 'Cidade'],
      ['João', '25', 'São Paulo'],
      ['Maria', '30', 'Rio de Janeiro'],
      ['Carlos', '35', 'Belo Horizonte']
  ]

with open('dados.csv', 'w') as arquivo:
    escritor = csv.writer(arquivo)
    for linha in dados:
      escritor.writerow(linha)
  