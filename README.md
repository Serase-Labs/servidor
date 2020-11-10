# Como rodar o servidor 🤔
Este arquivo vem com o básico para rodar não só o servidor do Serase, mas praticamente qualquer servidor Django com a estrutura padrão de arquivos.

Caso a quantidade de conteúdo deste arquivo te assuste, você pode pular para o [resumo](#📄-resumo), onde há apenas os códigos necessários.

O site [Django Girls](https://tutorial.djangogirls.org/pt/django_installation/) foi utilizado como referência para a criação deste documento.

## 🔧 Ferramentas 
Vamos começar instalando tudo que é necessário para rodar o servidor em sua máquina. Será necessário:

 - Python
 - Editor de texto/código *(recomendo o VS Code)*
 - Ferramenta Git *(o próprio Git ou GitKraken por exemplo)*

O *python* será utilizado para rodar o ambiente virtual e o servidor, o editor de texto para visualizar e editar o código do servidor e o Git para clonar o repositório em sua máquina e acessar uma branch específica (provavelmente a *dev* ou a *master*).

## 💻 Ambiente Virtual

Após clonar o repositório do servidor e instalar as ferramentas necessárias, devemos criar um ambiente virtual para rodar o servidor.

Um ambiente virtual ajuda a manter o ambiente de trabalho do seu computador organizado. Também ajuda a reconhecer melhor as dependências do seu projeto, uma vez que o ambiente virtual isola o código em si, fazendo com que o código do projeto não seja afetado e não afete outros projetos. Note então que este passo não é necessário mas **extremamente recomendado**.

Cada máquina terá seu próprio ambiente virtual, logo um ambiente virtual **não deve** ser commitado para o repositório. Para evitar esse erro, devemos criar um ambiente virtual diretamente na pasta principal do projeto e nomeá-lo como `myvenv` (nome padrão), desse jeito ele será ignorado pelo `.gitignore` do repositório do Serase.

Para criar o ambiente virtual em sua máquina, entre na pasta do projeto e digite na linha de comando:
```
D:\Repositorios\servidor> python3 -m venv myvenv
```
Sempre que fizermos alguma ação no servidor, é recomendado executar essa ação utilizando o ambiente virtual. Para acessar o ambiente é necessário digitar:
```
D:\Repositorios\servidor> myvenv\Scripts\activate
```
Você saberá que o ambiente está funcionando no momento que o console da linha de comando estiver com o prefixo `(myvenv)`.

Para desativar um ambiente virtual você pode fechar o console de linha de comando ou digitar `deactivate`.

Vale constar que o ambiente sempre se refere a versão correta do python, então você pode digitar `python` ao invés de `python3`.

## 📦 Pacotes 
Com o ambiente virtual ativo, devemos garantir que temos a versão mais recente do `pip`, que é o software que utilizaremos para instalar o Django e as dependências do projeto:
```
(myvenv) D:\Repositorios\servidor> python -m pip install --upgrade pip
```

O arquivo `requirements.txt` contém uma lista das dependências do projeto que serão instaladas no `pip install`. Ele está localizado na pasta principal do projeto. Para instalar as dependências, juntamente com o Django, basta rodar o comando:
```
(myvenv) D:\Repositorios\servidor> pip install -r requirements.txt
```
Caso a linha de comando congele ao tentar instalar o Django, você pode tentar rodar um versão alternativa do comando:
```
(myvenv) D:\Repositorios\servidor> python -m pip install -r requirements.txt
```

## ⚙️ Servidor
Agora que temos o ambiente virtual e o Django instalados corretamente na sua máquina, chegou a hora de rodar o servidor. Por padrão o servidor será executado na porta `8000`:
```
(myvenv) D:\Repositorios\servidor> python manage.py runserver
```

Agora você consegue acessar o servidor em `127.0.0.1:8000`. Para desativar o servidor basta apertar `ctrl+c` no console. 

## 📄 Resumo
Essa seção possui os códigos necessários para rodar o servidor. É recomendado ler as seções anteriores pelo menos uma vez e utilizar esse resumo para rodar o servidor nas próximas vezes. 


Instalar ambiente virtual *(opcional)*:

1. `python3 -m venv myvenv`

Instalar dependências:
1. `myvenv\Scripts\activate` *(ambiente virtual)*
2. `python -m pip install --upgrade pip`
3. `pip install -r requirements.txt`
4. `deactivate` *(ambiente virtual)*

Rodar o servidor:
1. `myvenv\Scripts\activate` *(ambiente virtual)*
2. `pip install -r requirements.txt` *(nova dependência)*
3. `python manage.py runserver`

Parar o servidor:
1. *ctrl + c*
2. `deactivate` *(ambiente virtual)*

