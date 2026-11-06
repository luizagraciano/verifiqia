from src.database.storage import create_activity

from src.database.storage import (
    get_activity_list,
    get_activity_content,
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
        activities = get_activity_list()

        activity_row = next(
            (item for item in activities if item[0] == activity_id),
            None
        )

        if activity_row is None:
            return None

        activity = dict(zip(
            ("id", "name", "description", "tag", "difficulty", "created_at"),
            activity_row
        ))

        content = get_activity_content(activity_id)

        content_data = dict(zip(
            ("id", "activity_id", "instruction", "answer", "resources"),
            content
        ))

        activity["instruction"] = content_data["instruction"]
        activity["answer"] = content_data["answer"]
        activity["resources"] = content_data["resources"]

        return activity

    except ValueError:
        return None


def edit_activity(
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

    fields = {
        "Título": name,
        "Descrição": description,
        "Tema": tag,
        "Dificuldade": difficulty,
        "Instruções": instruction,
        "Respostas": answer,
        "Recursos/orientações": resources
    }

    for field_name, value in fields.items():
        if not isinstance(value, str) or not value.strip():
            return {
                "success": False,
                "message": f"O campo {field_name} é obrigatório."
            }

    if not isinstance(activity_id, int) or activity_id <= 0:
        return {
            "success": False,
            "message": "ID da atividade inválido."
        }

    activity = get_activity(activity_id)

    if activity is None:
        return {
            "success": False,
            "message": "Atividade não encontrada."
        }

    try:
        update_activity(
            activity_id,
            name.strip(),
            description.strip(),
            tag.strip(),
            difficulty.strip(),
            instruction.strip(),
            answer.strip(),
            resources.strip()
        )

        updated_activity = get_activity(activity_id)

        if updated_activity is None:
            return {
                "success": False,
                "message": "Não foi possível confirmar a atualização."
            }

        return {
            "success": True,
            "message": "Atividade atualizada com sucesso."
        }

    except ValueError:
        return {
            "success": False,
            "message": "Erro ao atualizar a atividade."
        }