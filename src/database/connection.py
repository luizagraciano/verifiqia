import sqlite3
import os

# Define os caminhos para os arquivos de dados, schema e seed do banco de dados.
BASE_DIR = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATA_FILE = os.path.join(DATA_DIR, 'database.sqlite')
SCHEMA_FILE = os.path.join(DATABASE_DIR, 'schema.sql')
SEED_FILE = os.path.join(DATABASE_DIR, 'seed.sql')

# Abre a conexão SQLite da aplicação e garante que o diretório de dados exista.
def get_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    connection = sqlite3.connect(DATA_FILE)
    connection.row_factory = sqlite3.Row
    return connection


# Fecha a conexão recebida quando ela foi criada corretamente.
def close_db(connection):
    if connection:
        connection.close()


# Cria as tabelas do banco usando o script de schema configurado.
def init_db():
  connection = get_db()
  try:
    if os.path.exists(SCHEMA_FILE):
      with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        connection.executescript(f.read())
      connection.commit()
  finally:
    close_db(connection)


# Insere os dados iniciais no banco usando o script de seed configurado.
def seed_db():
  connection = get_db()
  try:
    if os.path.exists(SEED_FILE):
      with open(SEED_FILE, "r", encoding="utf-8") as f:
        connection.executescript(f.read())
      connection.commit()
  finally:
    close_db(connection)