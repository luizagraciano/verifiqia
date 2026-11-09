"""
VerifiQIA - História BIB-01: Acessar e localizar atividades salvas na biblioteca


"""

from imprimir_atividade import imprimir_atividade  # junção com a história IMP-01

# ---------------------------------------------------------------
# 1) DADOS DE TESTE
# Regra 1: só usuário autenticado acessa a biblioteca.
#   -> Aqui o login é SIMULADO (a história de Cadastro/Login é outra).
#   -> Para testar o acesso negado, troque True por False.
# Regra 2: toda atividade salva fica disponível offline.
#   -> Por enquanto as atividades ficam numa lista dentro do código.
#   -> Depois, elas virão do banco local (SQLite).
#   -> Para testar a biblioteca vazia (Cenário 3), troque a lista por [].
# ---------------------------------------------------------------
usuario_autenticado = True

atividades_salvas = [
    {
        "id": 1,
        "titulo": "Detetives de Notícias",
        "disciplina": "Língua Portuguesa",
        "ano": "7º",
        "objetivo": "Ensinar os alunos a identificar sinais de alerta em textos gerados por IA.",
        "enunciado": "Em grupos, analisem três textos curtos e decidam quais parecem confiáveis.",
        "passo_a_passo": [
            "Divida a turma em grupos de 4 alunos.",
            "Entregue três textos impressos para cada grupo.",
            "Cada grupo apresenta sua conclusão em 2 minutos.",
        ],
    },
    {
        "id": 2,
        "titulo": "Imagem Real ou Criada por IA?",
        "disciplina": "Artes",
        "ano": "8º",
        "objetivo": "Reconhecer pistas visuais de imagens criadas por inteligência artificial.",
        "enunciado": "Observem seis imagens impressas e classifiquem cada uma como real ou criada por IA.",
        "passo_a_passo": [
            "Espalhe as imagens pela mesa.",
            "Os alunos marcam real ou IA e justificam.",
            "Revele as respostas e converse sobre as pistas.",
        ],
    },
    {
        "id": 3,
        "titulo": "Quem Escreveu Isso?",
        "disciplina": "História",
        "ano": "9º",
        "objetivo": "Discutir a importância de checar fontes antes de compartilhar informações.",
        "enunciado": "Compare um texto de livro didático com um texto gerado por IA sobre o mesmo tema.",
        "passo_a_passo": [
            "Leiam os dois textos em duplas.",
            "Listem diferenças de fonte, autoria e precisão.",
            "Discutam como confirmar uma informação.",
        ],
    },
]


# ---------------------------------------------------------------
# 2) LISTAR AS ATIVIDADES
# Cenário 4: se a lista (já filtrada) estiver vazia, avisa o professor.
# ---------------------------------------------------------------
def listar_atividades(lista):
    print("\n--- BIBLIOTECA DE ATIVIDADES ---")
    if len(lista) == 0:
        print("Nenhuma atividade encontrada")
        return
    for numero, atividade in enumerate(lista, start=1):
        print(f"[{numero}] {atividade['titulo']} ({atividade['disciplina']}, {atividade['ano']} ano)")


# ---------------------------------------------------------------
# 3) BUSCAR / FILTRAR (Cenário 2)
# Procura o termo no título, na disciplina ou no ano.
# .lower() deixa tudo minúsculo para a busca não diferenciar maiúsculas.
# ---------------------------------------------------------------
def buscar_atividades(lista, termo):
    termo = termo.lower()
    encontradas = []
    for atividade in lista:
        texto = atividade["titulo"] + " " + atividade["disciplina"] + " " + atividade["ano"]
        if termo in texto.lower():
            encontradas.append(atividade)
    return encontradas


# ---------------------------------------------------------------
# 4) EXIBIR UMA ATIVIDADE COMPLETA (Cenário 1)
# Regra 3: ao selecionar, o sistema exibe e disponibiliza a ação "Imprimir".
# (A impressão em si vem do arquivo imprimir_atividade.py - história IMP-01.)
# ---------------------------------------------------------------
def exibir_atividade(atividade):
    # Devolve True se o professor pediu uma nova impressão (volta para a lista).
    # Devolve False se ele só quer voltar à biblioteca.
    while True:
        print("\n" + "=" * 50)
        print(atividade["titulo"].upper())
        print(f"{atividade['disciplina']} - {atividade['ano']} ano")
        print("=" * 50)
        print("Objetivo/Orientações:", atividade["objetivo"])
        print("Enunciado:", atividade["enunciado"])
        print("Passo a passo:")
        for numero, passo in enumerate(atividade["passo_a_passo"], start=1):
            print(f"  {numero}. {passo}")

        print("\n[1] Imprimir   [0] Voltar à biblioteca")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            # Função da história IMP-01: gera o arquivo, mostra sucesso ou erro
            # e pergunta se o professor quer uma nova impressão.
            quer_nova_impressao = imprimir_atividade(atividade)
            if quer_nova_impressao:
                return True
            # Se não quis (ou deu erro), a atividade continua na tela.
        elif opcao == "0":
            return False
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------
# 5) MENU DA BIBLIOTECA
# ---------------------------------------------------------------
def menu_biblioteca():
    # Regra 1: só usuário autenticado
    if not usuario_autenticado:
        print("Acesso negado. Faça login para acessar a biblioteca.")
        return

    # Cenário 3: biblioteca vazia
    if len(atividades_salvas) == 0:
        print("\nVocê ainda não tem atividades salvas")
        resposta = input("Deseja ir ao gerador de atividades? (s/n): ").strip().lower()
        if resposta == "s":
            print("(Aqui abriria o gerador de atividades)")
        return

    filtro = ""  # termo de busca atual (vazio = mostra tudo)

    while True:
        if filtro == "":
            resultado = atividades_salvas
        else:
            print(f"\nFiltro ativo: '{filtro}'")
            resultado = buscar_atividades(atividades_salvas, filtro)

        listar_atividades(resultado)

        print("\nDigite o número para abrir | [B] Buscar | [L] Limpar filtro | [V] Voltar")
        escolha = input("Escolha: ").strip().lower()

        if escolha == "v":
            return
        elif escolha == "b":
            filtro = input("Digite o termo de busca: ").strip()
        elif escolha == "l":
            filtro = ""
        elif escolha.isdigit() and 1 <= int(escolha) <= len(resultado):
            quer_nova_impressao = exibir_atividade(resultado[int(escolha) - 1])
            if quer_nova_impressao:
                filtro = ""  # limpa o filtro e mostra a lista completa
                print("\nEscolha outra atividade para imprimir.")
        else:
            print("Opção inválida.")



if __name__ == "__main__":
    menu_biblioteca()