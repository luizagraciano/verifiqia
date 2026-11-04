from src.database.storage import create_activity

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