# 📲 Requisições a partir do React Native

Como referenciado no documento [Como rodar o servidor 🤔](../README.md), para acessar o servidor em dispositivos da mesma rede local, isso inclui o React Native rodando pelo Expo, precisamos rodar o servidor no IP da nossa própria máquina. Como cada máquina possui um IP diferente, ficaria difícil ter um endereço definitivo para ser utilizado no React Native. Uma vez que o servidor estiver hospedado na nuvem, finalmente teremos um endereço definitivo, porém até lá precisamos encontrar uma maneira de obter o IP da sua máquina em nossa aplicação.

Felizmente, o Expo trás uma ferramenta que nos auxilia na obtenção do endereço de IP da máquina que está rodando o servidor Expo (não confundir com o servidor do Serase). O código abaixo exemplifica tal ferramenta.
```
import Constants from "expo-constants";
  
const { manifest } = Constants;
const servidor_host = manifest.debuggerHost.split(`:`).shift().concat(`:8000`);
```
Note que também adicionamos a porta do servidor ao endereço de IP, dessa maneira conseguimos o endereço completo do servidor e já podemos fazer chamadas para caminhos específicos.

## 😎 Sobre a Fetch API

O servidor do Serase utiliza respostas em JSON, dessa forma conseguimos manter uma comunicação fácil através de requisições Ajax.

Requisições Ajax normalmente eram feitas através da framework `jQuery` ou da interface nativa `XMLHttpRequest`, porém com a introdução de `Promise` na linguagem, foi incluída uma nova API nativa com o propósito de facilitar e estruturar a maneira que fazemos requisições Ajax em Javascript.

A API Fetch é totalmente baseada em promises, então é interessante pesquisar sobre o funcionamento de `Promise`, da sintaxe `async/await` e `try/catch` para o melhor entendimento da implementação, uma vez que tais assuntos não serão cobertos neste documento.

## 👋 Requisições com Fetch API

O funcionamento básico da API se consiste em informar o endereço do servidor, o método da requisição e os parâmetros a serem passados para o servidor. Note que este documento **não** leva a autenticação do usuário em consideração.

O formato de parâmetros passados para a API é:
```
fetch(URL[, opções])
```
Sendo `URL` uma string e `opções` um *objeto opcional* para especificar informações extras á requisição. As opções são diversas, porém falaremos apenas das opções `method` e `body`.

A opção `method` define qual será o método da sua requisição, no servidor do Serase só utilizamos o método GET, para consultas, e o método POST, para operações que afetam o banco de dados.

Já a opção `body` define os parâmetros a serem enviados ao servidor na requisição POST. Por mais que seja possível passar parâmetros por `body` em requisições GET, não é recomendado por uma questão de coerência. Sendo assim, para passar parâmetros nas requisições GET utilizamos de parâmetros pela URL.

No caso do `body`, passamos um objeto com os parâmetros necessários. Porém precisamos converter o objeto para string para conseguirmos mandar ao servidor. A seguir um exemplo de passagem de parâmetros pelo `body`:

```
fetch("http://192.168.x.x/caminho/", {
	method: "POST",
	body: JSON.stringify({parametro: 1})
});
```

Utilizamos a função `stringify` para converter o objeto em string. Lembre-se que cada caminho, cada view, requer parâmetros diferentes, certas views não requerem parâmetro algum, então cada caso as informações serão diferentes.

No caso do método GET, também é necessário comprimir os parâmetros em uma string, porém diferente do método POST, não podemos simplesmente converter um objeto em string pela função `stringify`.

A maneira de passar os parâmetros é por uma lista de parâmetros na própria URL, onde essa lista é especificada após o caminho, começando com um `?` e em seguida uma lista separada pelo caractere `&`, com a sintaxe `chave=valor`. Para melhor visualização veja um exemplo de uma requisição GET sem parâmetros e uma com parâmetros:

Requisição GET sem parâmetros
```
fetch("http://192.168.x.x/caminho/");
```

Requisição GET com parâmetros:
```
fetch("http://192.168.x.x/caminho/?categoria=Lazer&limite=5");
```

## 🤝 Respostas com Fetch API

Agora que sabemos como fazer uma requisição ao servidor utilizando a API Fetch, precisamos obter a resposta da requisição.

Como dito previamente neste documento, a Fetch API utiliza de `Promise`, e é com esta funcionalidade que acessamos a resposta do servidor. Ao fazer uma requisição, é retornado uma `Promise`. Esta `Promise` é cumprida no momento que o servidor retorna uma resposta, sendo o retorno da `Promise` um objeto representando essa resposta.
```
fetch("http://192.168.x.x/caminho/")
.then(res => console.log(res) )
```
O objeto de resposta contém informações sobre a requisição/resposta e métodos para a decodificação do conteúdo. No nosso caso, utilizaremos o método `res.json()` que irá retornar uma `Promise` que ao ser cumprida nos retornará a resposta do servidor no formato de um objeto.
```
fetch("http://192.168.x.x/caminho/")
.then(res => res.json() )
.then(obj=> console.log(obj) )
```

Os exemplos utilizaram a sintaxe `then` de `Promise`, porém conseguimos atingir o mesmo efeito com a sintaxe `async/await`, veja o exemplo:
```
async function requisicaoX(){
	let req = await fetch("http://192.168.x.x/caminho/"),
	obj = await req.json();
	console.log(obj);
}
```