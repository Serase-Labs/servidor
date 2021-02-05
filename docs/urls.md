# 📎 URLs do Servidor

|Método| Caminho | Utilização |
|--|--|--|
|GET|[/padroes/](#consultar-padrões)|Mostrar uma lista de padrões do usuário|padrões|
|POST|/padrao/|Alterar um padrão já existente|
|DELETE|/padrao/|Deletar um padrão especificado pelo usuário|
|GET|[/movimentacoes/](#listar-movimentações)|Pegar uma lista de movimentações do usuário|
|GET|[/movimentacao/{id}/](#consultar-uma-movimentação)|Mostrar informações de uma movimentação especifica do usuário|
|POST|/movimentacao/|Inserir movimentação do usuário|
|GET|[/saldo/](#consultar-saldo)|Retorna saldo total e mensal|
|GET|/categoria/|Retorna uma lista com todas as categorias cadastradas no servidor|
|GET|/usuario/|Retorna informações sobre o usuário logado|
|POST|/login/|Realiza login do usuário|
|GET|/logout/|Realiza logout do usuário logado|
|POST|/cadastro/|Realiza cadastro do usuário|
|GET|[/status/](#status-do-servidor)|Retorna resposta de status caso requisição ocorra com sucesso|

## Consultar padrões
**URL:** `/padroes/`
**Método:** `GET`

Retorna uma lista de padrões de movimentação do usuário logado. Essa lista pode ser filtrada pelo seu tipo.

|Parâmetro|Valor|
|--|--|
|tipo|Opcional. Quando especificado, filtra a lista apenas para o tipo especifico. Aceita: "receita" e "despesa".|


## Consultar uma movimentação
**URL:** `/movimentacao/{id}/`
**Método:** `GET`

Retorna um objeto com todas as informações de uma movimentação do usuário logado. É necessário que o id da movimentação seja informado, e caso esta movimentação não pertença ao usuário, nada será retornado.

|Parâmetro|Valor|
|--|--|
|id|O id da movimentação a ser consultada. A movimentação deve ser do usuário logado, caso o contrário nada será retornado.|


## Listar movimentações
**URL:** `/movimentacoes/`
**Método:** `GET`

Retorna uma lista de movimentações com suas informações simples para display, como: `descricao`, `data_lancamento`, `valor_pago` e `id`. Para conseguir informações detalhadas de uma movimentação, recomenda-se utilizar uma [consulta de movimentação](#consultar-uma-movimentação) com o `id` recebido pela listagem. 

|Parâmetro|Valor|
|--|--|
|tipo|Opcional. Filtra a lista apenas para o tipo especifico. Aceita: "receita" e "despesa".|
|categoria|Opcional. Filtra a lista para movimentações de uma categoria específica.|
|data_inicial|Opcional. Filtra a lista para movimentações com data igual ou posterior a data especificada.|
|data_final|Opcional. Filtra a lista para movimentações com data igual ou anterior a data especificada.|
|limite|Opcional. Especifica o limite de resultados por requisição, retornando uma resposta de paginação.|
|offset|Opcional. Utilizada juntamente com `limite`, define o offset da requisição. É setada por padrão nas urls `proxima` e `anterior` retornadas da resposta de paginação.|


## Consultar saldo
**URL:** `/saldo/`
**Método:** `GET`

Retorna o saldo de um mês específico e o saldo total nesse mês, ou seja, a soma de todas as movimentações até o mês específico, incluindo o próprio mês. O valor padrão do mês é o mês atual, sendo assim, o valor total será a soma de todas as movimentações feitas.

|Parâmetro|Valor|
|--|--|
|mes_ano|Opcional. Define um mês para consultar o saldo. Esse parâmetro também afeta o total, o limitando até o mês selecionado. O formato do parâmetro é: YYYY-MM.|


## Status do servidor
**URL:** `/status/`
**Método:** `GET`

Retorna uma resposta de status positiva caso a requisição tenha ocorrido com sucesso. Esse caminho serve para testar o funcionamento do servidor e das requisições ao servidor.