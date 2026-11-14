from src.database.storage import get_activity_by_id, get_activity_list

# ---------------------------------------------------------------
# 2) LISTAR AS ATIVIDADES
# Cenário 4: se a lista (já filtrada) estiver vazia, avisa o professor.
# ---------------------------------------------------------------
def carregar_atividades():
    try:
        return get_activity_list()
    except Exception as e:
        raise ValueError(f"{e}")


def carregar_atividade(activity_id):
    try:
        atividade = get_activity_by_id(activity_id)
        if not atividade:
            raise ValueError("Atividade não encontrada")
        return atividade
    except Exception as e:
        raise ValueError(f"{e}")


# ---------------------------------------------------------------
# 3) BUSCAR / FILTRAR (Cenário 2)
# Procura o termo no título, na disciplina ou no ano.
# .lower() deixa tudo minúsculo para a busca não diferenciar maiúsculas.
# ---------------------------------------------------------------
def buscar_atividades(lista, termo):
    termo = termo.lower()
    encontradas = []
    for atividade in lista:
        texto = atividade["name"] + " " + atividade["description"] + " " + atividade["difficulty"] + " " + atividade["tag"]
        if termo in texto.lower():
            encontradas.append(atividade)
    return encontradas

