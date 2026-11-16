from src.database.storage import get_offline_activity_list, get_offline_activity_list_by_tag, get_offline_activity_by_id

# As tags fixas do sistema
TAGS_SISTEMA = ["Ética", "Matemática", "Português", "História", "Ciências", "Geografia"]


def buscar_atividades_por_tag_offline(tag: str):
    """Busca as atividades no banco usando a função do arquivo storage.py"""
    if tag not in TAGS_SISTEMA:
        return []
        
    # Puxa a lista do banco
    try:
        atividades = get_offline_activity_list_by_tag(tag)
    except Exception as e:
        raise ValueError(f"{e}")

    # Se a função do storage.py retornar None (vazio), devolvemos uma lista vazia
    if not atividades:
        return []
        
    return atividades

def listar_atividades_offline():
    """Lista todas as atividades offline disponíveis."""
    try:
        return get_offline_activity_list()
    except Exception as e:
        raise ValueError(f"Erro ao listar atividades offline: {e}")


def carregar_atividade_offline(id):
    """Carrega uma atividade offline pelo ID."""
    try:
        atividade = get_offline_activity_by_id(id)
        if not atividade:
            raise ValueError("Atividade não encontrada")
        return atividade
    except Exception as e:
        raise ValueError(f"{e}")