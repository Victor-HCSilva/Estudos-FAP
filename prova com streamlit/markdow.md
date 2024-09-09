# Funções existentes separadas (imcompleto, pronto para uso - usando as tabelas banco_prova_fap_v3):
2024-09-07
- conecao_ao_banco[x]
- criar conta [x]
- verificar_conta   [X]
- deletar [x]
- extrato [x]
- encontrar id [x]
- transferencia [x]
- saldo [x]
- realizar transacao [x]
- deletar [x]
- movimentacoes [x]
- verificar_senha [x]
---
# Novas tabelas (completo):
- tabela1 campos
1 - id_cliente
2 - numero_da_conta
3 - nome
5 - _data_
6 - saldo
7 - senha
---
- tabela2 
1 - id_cliente
2 - tipo_de_opercao 

('D'=deposito,'S'=saldo,'T-id1->id2'=tranferência de id1 para id2)


3 - tipo_de_conta 
4 - _data_
5 - saldo

# Inserção de senha (completo e funcional):

 - acesso da conta apenas com senha correta


# Fazer

 - no arquivo têm uma linha separando aonde foi parado. Estou adontando colocar o nome do que cada bloco
if está fazendo. Estão faltando as funções mais complexas, faltam:

 - a implemantação da funcao movimentaçãoquando for criar uma conta ('NC', 'D'=depósito, 's' Saque,'id1->id2'=transferência.)
 - documentação. 
 - faltando tratamentos de erros, 
 - legibilidade 
 - interface amigável.
