# Afazeres do Servidor
Listagem dos afazeres da primeira entrega do servidor.

## Geral
-  Relatório 
	 - [ ] Definir views do relatório
	 - [ ] Definir respostas do relatório
	 - [ ] Criar app no Django para o relatório
	 - [ ] Implementar views do relatório
- Login (pra depois)
	- [ ] Pesquisar sobre implementação com Ajax
	- [ ] Implementar de fato
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
	- [ ] Descobrir como gerar o Saldo todo mês (pra depois, com o login)
	- [ ] Implementar geração de Saldo todo começo de mês
- Notificações
	- [ ] O que vamos fazer com as notificações?
	
## Views
- View Padrão de Movimentação
	- [x] Consultar
	- [ ] Inserir
	- [ ] Atualizar
	- [ ] Deletar
- View Movimentação
	- [x] Consultar
	- [ ] Inserir
	- [ ] Atualizar
	- [ ] Deletar 
- View Categoria
	- [ ] Consultar
- View Listar Movimentações
	- [x] Paginação 
	- [x] Filtrar por despesa/receita/ambos  
	- [x] Filtrar por período 
	- [x] Filtrar por categoria 
- View Consultar Saldo
	- [ ] ~~Filtrar período~~
	- [x] Consultar um mês-ano
	- [ ] Gerar saldo caso não exista
- View Consultar Usuário
	- [ ] Implementação da view