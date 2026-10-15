import sqlite3
import os
import click

BASE_DIR = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATA_FILE = os.path.join(DATA_DIR, 'database.sqlite')
SCHEMA_FILE = os.path.join(DATABASE_DIR, 'schema.sql')
SEED_FILE = os.path.join(DATABASE_DIR, 'seed.sql')

def get_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    connection = sqlite3.connect(DATA_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def close_db(connection):
    if connection:
        connection.close()


def init_db():
  connection = get_db()
  try:
    if os.path.exists(SCHEMA_FILE):
      with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        connection.executescript(f.read())
      connection.commit()
  finally:
    close_db(connection)


def seed_db():
  connection = get_db()
  try:
    if os.path.exists(SEED_FILE):
      with open(SEED_FILE, "r", encoding="utf-8") as f:
        connection.executescript(f.read())
      connection.commit()
  finally:
    close_db(connection)


@click.group()
def cli():
  pass


@cli.command("init-db")
def init_db_command():
  init_db()
  click.echo("Banco de dados foi inicializado.")


@cli.command("seed-db")
def seed_db_command():
  seed_db()
  click.echo("Banco de dados de atividades offline foi pré-carregado.")


if __name__ == "__main__":
  cli()
