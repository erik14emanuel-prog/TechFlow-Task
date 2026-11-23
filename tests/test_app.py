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
