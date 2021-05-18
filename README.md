# Cadastro de Ativos e Importação de Preços

Este diretório conta com 2 arquivos, um responsável pela criação do Banco de Dados em sqlite3 e outro com as devidas funções para gerenciamento e inserção de preços e ativos.

## Como Funciona?

Basta rodar a função createDB() e o Banco de Dados será criado com o nome de Ativos.db


## Uso

Depois de criado o Banco de dados podemos usar 3 funções vindas do arquivo Cadastros e Importacoes.py

Temos:
```python
cadastrarAtivo()
precoAtivo()
habilitarAtivo()
``` 
# Cadastro de ativos

```python
cadastrarAtivo(simbolo,nome,habilitado)
```
Essa função recebe 3 parâmetros os quais são respectivamente:

- simbolo
 
  Se refere ao simbolo ou ticket do Ativo como por exemplo:'B3SA3.SAO',

- nome
 
  Exemplos 'Brasil','Bolsa Balcão'

- habilitado
 
  Caso seja False, o Ativo será cadastrado e não recebera importação de preços 

  Caso seja True o Ativo será cadastrado e poderá ter importação de preços

# Importação de Ativos
```python
precoAtivo(simbolo)
```

Função que vai inserir na tabela o valor do dia atual e dos últimos 7 dias uteis referente ao preço do Ativo indicado, ou atualiza-los caso já existam valores cadastrados para aquele dia.

# Habilitação de Ativos
```python
habilitarAtivo(simbolo)
```

Esta função server para habilitar a importação de preços em ativos que estão com a opção 'habilitado' como False. 

(Obs: Caso seja usada em um ativo que já tenha o status 'habilitado' como True, a função desabilitará a e o valor de 'habilitado' para aquele Ativo será False)

# Dependências
- sqlite3
- requests
- datetime
