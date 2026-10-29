import click
from src.database.connection import init_db, seed_db
from src.interface.app import generate_activity

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


@cli.command("generate-activity")
def generate_activity_command():
  generate_activity()

if __name__ == "__main__":
  cli()
