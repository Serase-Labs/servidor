# Afazeres do Servidor
Listagem dos afazeres da primeira entrega do servidor.

## Geral
-  Relatório 
	- [x] Definir views do relatório
	- [x] Definir respostas do relatório
	- [x] Criar app no Django para o relatório
	- [x] Implementar views do relatório
- Login (pra depois)
	- [x] Pesquisar sobre implementação com Ajax
	- [x] Implementar de fato
	- [ ] Ajustar views
- Modo de usos
	- [ ] Saber o que fazer com dívidas/metas
	- [ ] Definir lógica de dívidas/metas
- Padrões de Movimentação
	- [ ] Descobrir como gerar uma cobrança todo mês (pra depois, com o login)
	- [ ] Implementar geração de cobrança baseada em padrões
	- [ ] Checar se a cobrança do padrão foi paga
- Saldo
	- [X] Implementar views visualizar saldo geral
	- [ ] ~~Descobrir como gerar o Saldo todo mês (pra depois, com o login)~~
	- [ ] ~~Implementar geração de Saldo todo começo de mês~~
	- [x] Saldo é gerado/adicionado a partir da criação de uma movimentação
- Notificações
	- [ ] O que vamos fazer com as notificações?
	
## Views
- View Padrão de Movimentação
	- [x] Consultar
	- [x] Inserir
	- [?] Atualizar
	- [x] Deletar
- View Movimentação
	- [x] Consultar
	- [x] Inserir
	- [ ] Atualizar
	- [ ] Deletar 
- View Categoria
	- [x] Consultar
- View Listar Movimentações
	- [x] Paginação 
	- [x] Filtrar por despesa/receita/ambos  
	- [x] Filtrar por período 
	- [x] Filtrar por categoria 
- View Consultar Saldo
	- [ ] ~~Filtrar período~~
	- [x] Consultar um mês-ano
	- [x] Gerar saldo caso não exista
- View Consultar Usuário
	- [x] Implementação da view