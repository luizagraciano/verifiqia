import pytest
import sqlite3
from src.database.connection import get_db
import src.database.storage as storage

# Prepara um banco SQLite em memória para cada teste e restaura o estado ao final.
@pytest.fixture(autouse=True)
def setup_and_teardown(monkeypatch):
    # Setup
    test_connection = sqlite3.connect(":memory:")
    test_connection.row_factory = sqlite3.Row

    test_connection.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            cpf TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS activity_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            tag TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS activity_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER NOT NULL,
            instruction TEXT NOT NULL,
            answer TEXT NOT NULL,
            resources TEXT NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES activity_list(id)
        );
    ''')
    test_connection.commit()

    monkeypatch.setattr(storage, "get_db", lambda: test_connection)
    monkeypatch.setattr(storage, "close_db", lambda connection: None)

    yield

    # Teardown
    test_connection.close()

# Fornece dados válidos para os testes de usuários.
@pytest.fixture()
def user_data():
    user_data = {
            "username": "testuser",
            "cpf": "12345678900",
            "email": "testuser@example.com",
            "password": "password123"
        }

    return user_data

# Fornece dados inválidos para validar as regras de criação de usuários.
@pytest.fixture()
def invalid_user_data():
    invalid_user_data = {
            "username": None,
            "cpf": None,
            "email": None,
            "password": None
        }

    return invalid_user_data

# Fornece dados válidos para criar uma atividade de teste.
@pytest.fixture()
def activity_data():
    activity_data = {
        "name": "Test Activity",
        "description": "This is a test activity.",
        "tag": "tag1",
        "difficulty": "easy",
        "instruction": "Follow the instructions.",
        "answer": "42",
        "resources": "Resource links here."
    }

    return activity_data

# Fornece uma segunda atividade para testes de filtros e listagens.
@pytest.fixture()
def activity_data2():
    activity_data2 = {
        "name": "Test Activity 2",
        "description": "This is another test activity.",
        "tag": "tag2",
        "difficulty": "medium",
        "instruction": "Follow the instructions for activity 2.",
        "answer": "43",
        "resources": "Resource links for activity 2."
    }

    return activity_data2

# Fornece uma terceira atividade para testes de filtros e listagens.
@pytest.fixture()
def activity_data3():
    activity_data3 = {
        "name": "Test Activity 3",
        "description": "This is yet another test activity.",
        "tag": "tag2",
        "difficulty": "hard",
        "instruction": "Follow the instructions for activity 3.",
        "answer": "44",
        "resources": "Resource links for activity 3."
    }

    return activity_data3

# Fornece os valores esperados após a atualização de uma atividade.
@pytest.fixture()
def updated_activity_data():
    updated_activity_data = {
        "name": "Updated Activity",
        "description": "This is an updated test activity.",
        "tag": "updated_test",
        "difficulty": "hard",
        "instruction": "Follow the updated instructions.",
        "answer": "45",
        "resources": "Updated resource links."
    }

    return updated_activity_data

# Fornece dados incompletos para validar falhas na criação de atividades.
@pytest.fixture()
def incomplete_activity_data():
    imcomplete_activity_data = {
            "name": None,
            "description": None,
            "tag": None,
            "difficulty": None,
            "instruction": None,
            "answer": None,
            "resources": None
        }
    
    return imcomplete_activity_data