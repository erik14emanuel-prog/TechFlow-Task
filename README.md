# TechFlow Tasks

Projeto acadêmico de Engenharia de Software da empresa fictícia TechFlow Solutions para uma startup de logística.

## Objetivo e escopo
Sistema web para criar, consultar, editar e excluir tarefas; definir prioridades (Baixa, Média, Alta); acompanhar status (A Fazer, Em Progresso, Concluído); e filtrar tarefas por status. A aplicação usa Flask e SQLite local. Não há autenticação, múltiplos usuários nem implantação em produção.

## Metodologia ágil
Kanban com três colunas: **To Do (A Fazer)**, **In Progress (Em Progresso)** e **Done (Concluído)**. Cada tarefa de desenvolvimento é representada por um card no GitHub Projects. A equipe acompanha o fluxo e revisa prioridades continuamente.

## Execução local
Requer Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m src.app
```

Abra http://127.0.0.1:5000 . O arquivo `tasks.db` é criado automaticamente.

## Testes e integração contínua

```bash
pytest -q
ruff check src tests
```

O workflow `.github/workflows/ci.yml` executa essas verificações em cada push e pull request. O status deve ser conferido na aba Actions após publicar.

## Gestão de mudanças — simulação documentada
**Escopo original:** CRUD de tarefas e definição de prioridade/status.
**Solicitação adicional:** filtro de tarefas por status.
**Justificativa:** a startup precisa localizar rapidamente tarefas pendentes ou concluídas, sem percorrer toda a lista.
**Impacto:** criação de rota de listagem filtrada, controle visual e teste automatizado. O novo card `feat: filtrar tarefas por status` deve ser adicionado ao Kanban e movido para Done após validação. O histórico Git deve conter um commit real dessa funcionalidade.

## Estrutura
- `src/`: lógica da aplicação e persistência SQLite
- `templates/`: páginas HTML
- `tests/`: testes automatizados
- `docs/`: diagramas, backlog e instruções de entrega
- `.github/workflows/`: CI

## Limitações e boas práticas
Protótipo acadêmico de usuário único, sem login; não usar para dados sensíveis. Consultas SQL parametrizadas e validação de entradas são aplicadas nas rotas. Para produção seriam necessários autenticação, proteção CSRF, autorização, logs e infraestrutura adequada.


## Gestão de mudanças

Durante o desenvolvimento, foi identificada a
necessidade de facilitar a identificação de
tarefas críticas pela equipe de logística.

Por esse motivo, foi proposta uma alteração
no escopo inicial: implementar um filtro de
tarefas por prioridade (Alta, Média e Baixa).

A solicitação foi registrada no GitHub Projects
e será implementada e validada por testes
automatizados antes de ser considerada concluída.

Essa mudança demonstra a aplicação de
metodologias ágeis, permitindo adaptar o
produto às necessidades do cliente.





