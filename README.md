# 🌐 Servidor do Serase

> Projeto de TCC do terceiro ano de informático do Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG).

Esse repositório abriga os códigos e documentação do servidor da aplicação Serase. O servidor atua como uma API Rest e possuí autenticação baseada em *Token*. Os documentos referentes a documentação estão presentes no diretório `/docs/`.

Saiba como rodar o servidor no arquivo [como_rodar.md](./docs/como_rodar.md)!

**Versão atual:** 👝 `bitcoin`
---

**Nome da versão:** `bitcoin`
**Data de lançamento:** `29/03/2021`

Esta versão inclui:
- Views separadas em apps diferentes com o propósito de melhorar a organização de código
- Deleção de códigos desnecessários
- Organização de pastas
- Usuário não necessita de username
- Nome do usuário armazenado no campo certo
- Validação de campos nas requisições
- Informações detalhadas de campos em resposta de erro
- Inclusão de pagamento extra a um padrão
- Correção de erros nos códigos anteriores


**Versão Anterior:** 👛 `pre-bitcoin`
---

**Nome da versão:** `pre-bitcoin`
**Data de lançamento:** `22/03/2021`

Esta versão inclui:
- Login/Cadastro utilizando autenticação `Token`
- Categorias de movimentação pré-definidas
- Adição e gerenciamento de movimentações simples
- Armazenamento do saldo mensal do usuário
- Relatórios sobre as movimentações realizadas pelo usuário em um determinado período
- Adição e gerenciamento de padrões de movimentação, ou seja, movimentações fixas
- Geração dinâmica de cobranças a partir de padrões de movimentação
- Cadastro de uma dívida e inclusão como padrão de movimentação variado
- Documentação parcial quanto a URLs gerais e relatórios