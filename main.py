import click
from src.database.connection import init_db, seed_db

@click.group()
# Agrupa os comandos de linha de comando disponíveis para a aplicação.
def cli():
  pass


@cli.command("init-db")
# Inicializa as tabelas do banco de dados a partir do schema definido no projeto.
def init_db_command():
  init_db()
  click.echo("Banco de dados foi inicializado.")


@cli.command("seed-db")
# Carrega no banco os dados iniciais de atividades disponíveis offline.
def seed_db_command():
  seed_db()
  click.echo("Banco de dados de atividades offline foi pré-carregado.")


if __name__ == "__main__":
  cli()
