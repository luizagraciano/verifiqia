from src.database.storage import get_activity_by_id, get_activity_list, get_activity_content, get_activity_list_by_tag
from .exporter import imprimir_atividade  # junção com a história IMP-01

usuario_autenticado = True


# ---------------------------------------------------------------
# 2) LISTAR AS ATIVIDADES
# Cenário 4: se a lista (já filtrada) estiver vazia, avisa o professor.
# ---------------------------------------------------------------
def carregar_atividades():
    try:
        return get_activity_list()
    except Exception as e:
        raise ValueError(f"{e}")
     

def listar_atividades(lista):
    print("\n--- BIBLIOTECA DE ATIVIDADES ---")
    if len(lista) == 0:
        print("Nenhuma atividade encontrada")
        return
    for numero, atividade in enumerate(lista, start=1):
        print(
            f"[{numero}] {atividade['name']} "
            f"({atividade['description']}, {atividade['difficulty']}, {atividade['tag']})"
        )


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

