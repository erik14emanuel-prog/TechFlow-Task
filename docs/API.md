
# Documentação Técnica — TechFlow Tasks

## 1. Visão geral

O TechFlow Tasks é um sistema web de gerenciamento
ágil de tarefas desenvolvido em Python com Flask
e banco de dados SQLite.

O sistema permite organizar atividades de equipes
de logística, utilizando prioridades e status.

## 2. Funcionalidades

- Cadastrar novas tarefas
- Listar tarefas cadastradas
- Editar informações de tarefas
- Excluir tarefas
- Filtrar tarefas por status
- Filtrar tarefas por prioridade
- Combinar filtros de status e prioridade
- Validar informações enviadas pelo usuário

## 3. Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | / | Lista e filtra tarefas |
| POST | /tasks | Cadastra uma tarefa |
| GET | /tasks/{id}/edit | Exibe formulário de edição |
| POST | /tasks/{id}/edit | Atualiza uma tarefa |
| POST | /tasks/{id}/delete | Exclui uma tarefa |

## 4. Estrutura dos dados

Cada tarefa possui:

- id: identificador único
- title: título da tarefa
- description: descrição
- priority: Baixa, Média ou Alta
- status: A Fazer, Em Progresso ou Concluído
- created_at: data e hora de criação

## 5. Regras de validação

- O título é obrigatório.
- O título aceita até 120 caracteres.
- A descrição aceita até 1000 caracteres.
- A prioridade deve possuir um valor válido.
- O status deve possuir um valor válido.
- Tarefas inexistentes retornam erro HTTP 404.
- Entradas inválidas retornam erro HTTP 400.

## 6. Segurança

O sistema utiliza consultas SQL parametrizadas
para reduzir o risco de SQL Injection.

Os dados recebidos são validados antes de
serem armazenados no banco de dados.

## 7. Controle de qualidade

O projeto utiliza Pytest para executar testes
automatizados.

O GitHub Actions executa os testes a cada
push e pull request, permitindo identificar
falhas durante o desenvolvimento.

## 8. Mudança de escopo

Foi implementado um filtro adicional por
prioridade para facilitar a identificação
de tarefas críticas.

A alteração foi registrada no GitHub Projects,
implementada no código e validada por testes.
