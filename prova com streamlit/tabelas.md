# tabelas sql

- tabela 1
use prova_fap;
create table if not exists banco(
id_cliente int auto_increment primary key,
numero_da_conta int unique,
nome varchar(50),
_data_ date,
saldo decimal(10,2),
senha int 
);

- tabela 2
create table movimentacoes(
id_cliente int,
tipo_de_operacao VARCHAR(15),
tipo_de_conta VARCHAR(20),
_data_ date,
saldo decimal(10,2)
);