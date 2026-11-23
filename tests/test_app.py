import sqlite3
import pytest
from src.app import create_app

@pytest.fixture
def client(tmp_path):
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'test.db')})
    return app.test_client()

def test_home(client):
    assert client.get('/').status_code == 200

def test_create_and_list(client):
    response = client.post('/tasks', data={'title': 'Separar pedidos', 'priority': 'Alta', 'status': 'A Fazer'})
    assert response.status_code == 302
    assert b'Separar pedidos' in client.get('/').data

def test_reject_empty_title(client):
    assert client.post('/tasks', data={'title': '  '}).status_code == 400

def test_reject_invalid_priority(client):
    assert client.post('/tasks', data={'title': 'Teste', 'priority': 'Urgentissima'}).status_code == 400

def test_edit_and_filter(client):
    client.post('/tasks', data={'title': 'Inicial'})
    response = client.post('/tasks/1/edit', data={'title': 'Atualizada', 'priority': 'Alta', 'status': 'Concluído'})
    assert response.status_code == 302
    assert b'Atualizada' in client.get('/?status=Conclu%C3%ADdo').data
    assert b'Atualizada' not in client.get('/?status=A+Fazer').data

def test_delete(client):
    client.post('/tasks', data={'title': 'Remover'})
    assert client.post('/tasks/1/delete').status_code == 302
    assert b'Remover' not in client.get('/').data

def test_missing_task(client):
    assert client.get('/tasks/999/edit').status_code == 404
    assert client.post('/tasks/999/delete').status_code == 404



def test_filter_by_priority(client):
    """Verifica se o filtro retorna somente a prioridade escolhida."""
    client.post('/tasks', data={
        'title': 'Entrega urgente',
        'priority': 'Alta'
    })
    client.post('/tasks', data={
        'title': 'Organizar documentos',
        'priority': 'Baixa'
    })

    response = client.get('/?priority=Alta')

    assert response.status_code == 200
    assert b'Entrega urgente' in response.data
    assert b'Organizar documentos' not in response.data


def test_filter_by_priority_and_status(client):
    """Verifica a combinação dos filtros de prioridade e status."""
    client.post('/tasks', data={
        'title': 'Pedido prioritario pendente',
        'priority': 'Alta',
        'status': 'A Fazer'
    })
    client.post('/tasks', data={
        'title': 'Pedido prioritario concluido',
        'priority': 'Alta',
        'status': 'Concluído'
    })
    client.post('/tasks', data={
        'title': 'Pedido comum pendente',
        'priority': 'Baixa',
        'status': 'A Fazer'
    })

    response = client.get(
        '/?priority=Alta&status=A+Fazer'
    )

    assert response.status_code == 200
    assert b'Pedido prioritario pendente' in response.data
    assert b'Pedido prioritario concluido' not in response.data
    assert b'Pedido comum pendente' not in response.data


def test_show_all_tasks_without_filters(client):
    """Verifica se todas as tarefas aparecem sem filtros."""
    client.post('/tasks', data={
        'title': 'Tarefa de prioridade alta',
        'priority': 'Alta'
    })
    client.post('/tasks', data={
        'title': 'Tarefa de prioridade baixa',
        'priority': 'Baixa'
    })

    response = client.get('/')

    assert response.status_code == 200
    assert b'Tarefa de prioridade alta' in response.data
    assert b'Tarefa de prioridade baixa' in response.data


def test_reject_title_over_120_characters(client):
    """Rejeita títulos acima do limite permitido."""
    response = client.post('/tasks', data={
        'title': 'A' * 121,
        'priority': 'Alta',
        'status': 'A Fazer'
    })

    assert response.status_code == 400


def test_reject_description_over_1000_characters(client):
    """Rejeita descrições acima do limite permitido."""
    response = client.post('/tasks', data={
        'title': 'Tarefa de teste',
        'description': 'A' * 1001
    })

    assert response.status_code == 400


def test_reject_title_with_only_spaces(client):
    """Impede cadastro com título contendo apenas espaços."""
    response = client.post('/tasks', data={
        'title': '     '
    })

    assert response.status_code == 400
