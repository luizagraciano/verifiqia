import click
from src.database.connection import init_db, seed_db
from src.interface.app import generate_activity, main_menu, edit_activity, menu_biblioteca, delete_activity

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

@cli.command("main-menu")
# Inicia o fluxo interativo de geração de atividades com inteligência artificial.
def main_menu_command():
  main_menu()

@cli.command("generate-activity")
# Inicia o fluxo interativo de geração de atividades com inteligência artificial.
def generate_activity_command():
  generate_activity()

@cli.command("edit-activity")
# Inicia o fluxo interativo de edição de atividades com inteligência artificial.
def edit_activity_command():
  # Solicita ao usuário o ID apenas para fins de teste rápido
  activity_id = click.prompt("Digite o ID da atividade que deseja editar")
  edit_activity(activity_id)

@cli.command("library")
# Inicia o fluxo interativo de geração de atividades com inteligência artificial.
def library_command():
  menu_biblioteca()

@cli.command("delete-activity")
# Inicia o fluxo interativo de exclusão de atividades com inteligência artificial.
def delete_activity_command():
  # Solicita ao usuário o ID apenas para fins de teste rápido
  activity_id = click.prompt("Digite o ID da atividade que deseja excluir")
  delete_activity(activity_id)

if __name__ == "__main__":
  cli()
