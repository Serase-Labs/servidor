# Padrões de Resposta
Tipos de padrões de respostas:
- [Resposta com conteúdo](#resposta-com-conteúdo)
- [Resposta de status](#resposta-de-status)
- [Resposta com lista](#resposta-com-lista)
- [Resposta de paginação](#resposta-de-paginação)

**Nota aos desenvolvedores do back-end:**
Este arquivo apenas comenta sobre as respostas e o que é cada parâmetro/valor esperado, porém não é necessário implementar o padrão manualmente uma vez que há funções de auxilio no arquivo `serase_app/padroes_resposta.py`.


## Resposta com conteúdo
Quando se espera um conteúdo como resposta, o padrão de resposta é o seguinte:

    {
	    status: 200,             // status da requisicao
	    conteudo: qualquer_valor // conteúdo da resposta
    }

## Resposta de Status
Quando a resposta não possui conteúdo, ela deve responder com uma mensagem de feedback, tanto positivo caso a operação tenha ocorrido com sucesso, quanto negativo caso ocorra algum erro. O padrão de respostas de status é o seguinte: 

    {
	    status: 200,  // status da requisicao
	    mensagem: ""  // mensagem com feedback da operação
    }

## Resposta com lista
Grande parte das requisições esperam multiplos valores, para isso temos as respostas com lista. As diferenças entre uma resposta com lista e uma [resposta com conteúdo](#resposta-com-conteúdo) é apenas um valor extra que informa a quantidade de itens retornados.

    {
	    status: 200,        // status da requisicao
	    conteudo: {} ou [], // conteúdo da resposta
	    total: 20           // quantidade de itens retornados
    }



## Resposta de paginação
Diferente de uma [resposta com lista](#resposta-com-lista), uma resposta de paginação é uma *resposta complexa* e acrescenta diversos valores a seu corpo. Dessa maneira, é necessário um controle da paginação para que fique organizada e facil de entender para ambos os lados (cliente e desenvolvedor). 

Este sistema de paginação foi baseado no sistema de paginação da API Rest do Spotify.  

### Parâmetros da requisição
Valores a serem passados na requisição.  Há possibilidade que requisições especificas possuam parâmetros especificos, porém caso a requisição seja de paginação, tais parâmetros são obrigatórios.

|Parâmetro  | Valor |
|--|--|
| limite |  A quantidade limite de itens a serem retornados na requisição.|
| offset| Opcional. O index do primeiro item a ser retornado. Por padrão o index é 0, ou seja, o primeiro item.|

### Valores da resposta
A resposta de paginação é bem detalhada e a maioria dos valores só são utilizados em casos muito especificos. Mesmo assim, é interessante manter tais valores caso haja uma necessidade de uso.

|Nome| Tipo | Descrição |
|--|--|--| 
| status | int | Status da requisição (padrão) |
| conteudo | vetor de objetos | Lista dos itens retornados |
| total | int | Total de itens disponiveis a requisição.|
| limite | int | O número máximo de itens por requisição. *(definido na requisição)* |
| offset | int | O offset do itens retornados. *(definido na requisição ou por padrão)* |
| proxima | url | URL da próxima página de itens. *(se nenhuma, `null`)* |
| anterior | url | URL da página anterior de itens. *(se nenhuma, `null`)* |

### Exemplo de resposta
		
	{
	    status: 200, 
	    conteudo: [ ],
	    total: 65,
	    limite: 10,
	    offset: 0,
	    proxima: "/url?offset=20&limit=20", 
	    anterior: null
    }

