## Código: Sistema Bancário Simples 

Este código implementa um sistema bancário simples usando Streamlit e MySQL puro sem ORM (object relational model). Ele permite aos usuários criar contas, fazer depósitos, saques, transferências e visualizar extratos. O código está dividido em três partes principais:

**Para usar este sistema, você precisará:**

1. Criar um banco de dados MySQL e tabelas.
2. Criar um arquivo *.env* com as variáveis de ambiente necessárias para a conexão com o banco de dados.
3. Instalar as dependências necessárias: *mmysql-connector-python*, *streamlit*, *dotenv*.

### Bibliotecas usadas:

 
 ```
pip install mysql-connector-python
pip install streamlit
pip install dotenv
 ```
### Versões dos programas usados
 - MySQL
```
MySQL Workbench versão 8.0
```
 - Python - Bibliotecas:
```
print("Versão do Python",platform.python_version())#-->> 3.12.4
print('Versão da biblioteca mysql.connector:', mysql.connector.__version__)#-->> mysql-connector-python -->>9.0.0
print('versão do streamlit', st.__version__)#-->>1.32.0'
```

### Tabelas no MySQL usadas:


```
use prova_fap;
create table if not exists banco(
id_cliente int auto_increment primary key,
numero_da_conta int unique,
nome varchar(50),
_data_ date,
saldo decimal(10,2),
senha int 
);

create table movimentacoes(
id_cliente int,
tipo_de_operacao VARCHAR(15),
tipo_de_conta VARCHAR(20),
_data_ date,
saldo decimal(10,2)
);

```

**1. Funções auxiliares de conexão e lógica de banco de dados:**

-  **conexao_ao_banco()**: Esta função conecta o sistema ao banco de dados MySQL. Ela utiliza as variáveis de ambiente *host*, *database*, *user* e *password* definidas no arquivo *.env* para estabelecer a conexão.

- **novo_numero()**: Gera um novo número de conta aleatório entre 10000 e 99999, garantindo que ele não esteja em uso.

* **verificar_senha(numero_da_conta)**: Verifica se a senha inserida pelo usuário corresponde à senha associada à conta.

-  **exibir_nome(numero_da_conta)**: Retorna o nome do titular da conta.

- **_salario(numero_da_conta)**: Retorna o saldo da conta.

- **encontrar_id(numero_da_conta)**: Retorna o ID do cliente associado à conta.

- **movimentacoes(saldo, tipo_de_operacao, tipo_de_conta, id_cliente)**: Registra as movimentações da conta no banco de dados.

-  **transacoes(numero_da_conta, valor, tipo_de_transacao)**: Realiza depósitos e saques na conta do usuário.

- **transferencia(valor, numero_do_beneficiado, numero_da_conta)**: Realiza transferências entre contas.

- **deletar(numero_da_conta)**: Exclui a conta do banco de dados.

- **extrato(numero_da_conta)**: Gera o extrato da conta do usuário.

**2. Interface Streamlit:**

- **main()**: Função principal que define a interface do usuário.

- **st.title("Sistema Bancário simples")**: Define o título da aplicação.

- **st.sidebar.selectbox("Menu", menu)**: Cria um menu lateral com as opções "Possuo Conta", "Não possuo Conta" e "Sair".

- **if escolha == "Possuo Conta"**: Bloco de código que lida com o fluxo de usuários com contas existentes.

    - **Login**: Solicita o número da conta e a senha do usuário.
    - **Verificação de senha**: Verifica a senha e autentica o usuário.
    - **Menu de operações**: Apresenta um menu com as opções "Depositar", "Sacar", "Extrato", "Transferência", "Deletar Conta" e "Sair".
    - **Implementação de operações**: Realiza as operações selecionadas pelo usuário, chamando as funções apropriadas.

- **elif escolha == "Não possuo Conta"**: Bloco de código que lida com o fluxo de criação de novas contas.

    - **Solicitação de dados**: Coleta informações como nome, saldo inicial, senha, data e tipo de conta do usuário.
    - **Criação da conta**: Cria a conta no banco de dados, atribuindo um novo número de conta e registrando as informações do usuário.
    

- **elif escolha == "Sair"**: Desloga o usuário da sessão.

**3. Inicialização do Streamlit:**

- **load_dotenv()**: Carrega as variáveis de ambiente do arquivo *.env*.

- **if __name__ == '__main__':**: Executa a função *main()* quando o script é executado.

**Observações:**

* O código utiliza o estado da sessão do Streamlit (*st.session_state*) para armazenar o status de login do usuário.
* O sistema é baseado em um banco de dados MySQL, que armazena as informações de conta e as movimentações dos usuários.
* A segurança do sistema é limitada, pois as senhas são armazenadas em texto simples no banco de dados. É recomendável implementar mecanismos de criptografia para proteger as senhas.

4. Executar o script Python.

##### Observação: Este código é apenas um exemplo básico. Para ter um sistema mais robusto e seguro é indicado:

* Criptografia de senhas;
* Gerenciamento de múltiplos tipos de contas;
* Taxas e juros;
* Integração com outros sistemas.




