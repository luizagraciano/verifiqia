import click
from src.database.connection import init_db, seed_db

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
