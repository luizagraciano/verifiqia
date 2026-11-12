
from src.database.storage import create_activity
from src.database.storage import (
    get_activity_by_id,
    update_activity
)

def save_activity_to_database(activity):

    # Valida se o dicionário de atividade existe antes de tentar salvar no banco de dados.
    if not activity:
        raise ValueError("Nenhuma atividade gerada para salvar. Gere uma atividade primeiro.")

    # Desempacota os campos da atividade em variáveis individuais para envio ao banco de dados.
    name = activity["name"]
    description = activity["description"]
    tag = None
    difficulty = activity["difficulty"]
    instruction = activity["instruction"]
    answer = activity["answer"]
    resources = activity["resources"]

    # Tenta salvar a atividade no banco de dados usando.
    try:
        create_activity(name, description, tag, difficulty, instruction, answer, resources)

    except Exception as e:
        raise ValueError(f"Erro ao salvar a atividade no banco de dados: {e}")



def get_activity(activity_id):
    """
    Busca uma atividade pelo ID e retorna seus dados,
    incluindo instruções, respostas e recursos.
    """
    try:
        return get_activity_by_id(activity_id)
    except (TypeError, ValueError):
        return None


def edit_activity_in_database(
    activity_id,
    name,
    description,
    tag,
    difficulty,
    instruction,
    answer,
    resources
):
    """
    Edita uma atividade existente.
    Retorna uma mensagem de sucesso ou de erro.
    """
   
    try:
        activity_id = int(activity_id)
    except (TypeError, ValueError):
        raise ValueError("ID da atividade inválido.")

    if activity_id <= 0:
        raise ValueError("ID da atividade inválido.")
        

    activity = get_activity(activity_id)
    if activity is None:
        raise ValueError("Atividade não encontrada.")

    try:
        update_activity(
            activity_id,
            name,
            description,
            tag,
            difficulty,
            instruction,
            answer,
            resources
        )

        updated_activity = get_activity(activity_id)

        if updated_activity is None:
            raise ValueError("Erro ao recuperar a atividade atualizada.")
        else:
            print("\nAtividade atualizada com sucesso.\n")
            return updated_activity

    except Exception as e:
        raise ValueError(f"Erro ao atualizar a atividade: {e}")