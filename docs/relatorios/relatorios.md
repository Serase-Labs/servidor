# Relatórios
O aplicativo do Serase possui três relatórios disponíveis para o acesso do usuário. Os relatórios podem ser **semanais**, **mensais** e **anuais**, onde cada um exibe informações pertinentes ao seu período. Essas informações são exibidas no relatório através de componentes.

Um relatório é composto de múltiplos componentes/análises. Então, podemos resumir um relatório como uma lista de análises, porém para uma melhor organização de ambas as partes (front-end e back-end) iremos tratar com um objeto de análises, onde os valores são os próprios componentes e as chaves sendo o nome de cada análise.
## Relatório da Semana
O relatório da semana é o relatório mais simples do sistema. 

Componentes:

 - **Relatório Resumo:** Resumo do valor das movimentações da semana.
 - **Relatório Análises:** Análise de categoria em relação aos gastos da semana. 
 - **Relatório Gráfico Semanal:** Informações para a geração do gráfico de valor gasto por dia da semana.

```
{
	resumo: {
		gasto_total: -5.5,
		receita_total: 156.7,
		fluxo_total: 151.2
	},
	analises: {
		maior_despesa: "Lazer",
		maior_salto: "Alimentação",
		maior_economia: "Transporte"
	},
	grafico_semanal: [
		{dia: 1, receita: 0, despesa: -350.5},
		{dia: 2, receita: 0, despesa: 0},
		{dia: 3, receita: 25.6, despesa: -7.9},
		{dia: 4, receita: 10, despesa: 0},
		{dia: 5, receita: 0, despesa: -500.6},
		{dia: 6, receita: 0, despesa: 0},
		{dia: 7, receita: 2365.5, despesa: 0}
	]
}
```


## Relatório do Mês
Componentes:
 - **Relatório Resumo:** Resumo do valor das movimentações do mês.
 - **Relatório Análises:** Análise de categoria em relação aos gastos do mês.

```
{
	resumo: {
		gasto_total: -5.5,
		receita_total: 156.7,
		fluxo_total: 151.2
	},
	analises: {
		maior_despesa: "Lazer",
		maior_salto: "Alimentação",
		maior_economia: "Transporte"
	}
}
```

Possíveis chamadas:
- **Relatório Gráfico Categoria:** Retorna porcentagem de despesa por categoria do mês.
- **Relatório Gráfico Padrão de Despesa:** Retorna porcentagem de despesa por padrão de despesa do mês.
- **Relatório Gráfico Mensal de Despesa:** Retorna quantidade de despesas de cada dia do mês.

*(O retorno de cada uma das análises opcionais pode ser visto no arquivo de componentes)*

## Relatório do Ano
Componentes:
 - **Relatório Resumo:** Resumo do valor das movimentações do ano.
 - **Relatório Análises:** Análise de categoria em relação aos gastos do ano.
 - **Gráfico Anual de Saldo:** Informações para a geração do gráfico de variação do saldo ao longo do ano.
 - **Gráfico Anual de Despesa Fixa:** Variação de cada despesa fixa variavel ao longo do ano.

```
{
	resumo: {
		gasto_total: -5.5,
		receita_total: 156.7,
		fluxo_total: 151.2
	},
	analises: {
		maior_despesa: "Lazer",
		maior_salto: "Alimentação",
		maior_economia: "Transporte"
	},
	grafico_saldo: [
		{mes: 1, valor: 576.2},
		{mes: 2, valor: 58.5},
		{mes: 3, valor: 2400.2},
		{mes: 4, valor: -916.9},
		{mes: 5, valor: 136.7},
		...
		{mes: 12, valor: 603.1},
	],
	grafico_despesa_fixa: {
		"Conta de Luz": [
			{mes: 1, valor: 576.2},
			{mes: 2, valor: 585.5},
			...
			{mes: 12, valor: 603.1},
		],
		"Telefone Fixo": [ ... ],
		...
	}
}
```

Possíveis chamadas:
- **Relatório Gráfico Categoria:** Retorna porcentagem de despesa por categoria do ano.
- **Relatório Gráfico Padrão de Despesa:** Retorna porcentagem de despesa por padrão de despesa do ano.

*(O retorno de cada uma das análises opcionais pode ser visto no arquivo de componentes)*