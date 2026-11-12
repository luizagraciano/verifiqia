from src.services.exporter import imprimir_atividade
from src.services.activity import save_activity_to_database
from src.services.ai_integration import generate_activity_with_ai
from src.services.library import buscar_atividades, carregar_atividades, listar_atividades


# Exibe o menu principal da aplicação e direciona para os fluxos de geração de atividades ou biblioteca de atividades.
def main_menu():

    print("\n============= Bem-vindo ao VerifiQIA =============")

    while True:
        print("\n================= Menu Principal =================")
        print("\nEscolha uma das opções abaixo para continuar:")
        print("[1] Gerar atividade com inteligência artificial")
        print("[2] Acessar biblioteca de atividades")
        print("[3] Sair")

        choice = input("\nDigite apenas o número: ").strip()

        if choice == "1":
            generate_activity()
        elif choice == "2":
            print("\nIndo para a biblioteca de atividades...")
            menu_biblioteca()
        elif choice == "3":
            print("\nSaindo do programa...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")
            continue


# Solicita os parâmetros ao usuário e controla o fluxo de geração da atividade.
def process_input(subject, grade, difficulty, theme, input_processed, activity):

    if not input_processed:
        while True:
            try:
                subject, grade, difficulty, theme = input("\nDigite o prompt com a disciplina, ano escolar, nível de dificuldade e tema, separados por vírgula, para gerar a atividade: ").split(",")
                subject, grade, difficulty, theme = subject.strip(), grade.strip(), difficulty.strip(), theme.strip()
                print("\nAguarde, gerando atividade...\n")
                input_processed = True
                break

            except ValueError:
                print("\nCertifique-se de fornecer todos os parâmetros separados por vírgula.")

    try:
        # Gera a atividade e apresenta seus campos no terminal.
        activity = generate_activity_with_ai(subject, grade, difficulty, theme)

        print(activity['name'])
        print(activity['description'])
        print(activity['difficulty'])
        print(activity['instruction'])
        print(activity['answer'])
        print(activity['resources'])

    except ValueError as e:
        print(f"\nErro: {e}")

    return subject, grade, difficulty, theme, input_processed, activity
    

# Exibe as opções disponíveis para continuar o fluxo da atividade.
def generate_activity(from_library=False):

    input_processed = False
    subject, grade, difficulty, theme, activity = None, None, None, None, None

    print("\n========== Gerador de Atividades com IA ==========")
    subject, grade, difficulty, theme, input_processed, activity = process_input(subject, grade, difficulty, theme, input_processed, activity)

    while True:
        print("\n========== Menu de Geração de Atividade ==========")
        print("\nEscolha uma das opções abaixo para continuar:")
        print("[1] Gerar nova atividade")
        print("[2] Reenviar o último prompt")
        print("[3] Salvar a última atividade gerada com sucesso")
        print("[4] Ir para a biblioteca de atividades")
        print("[5] Sair do módulo de geração de atividades")

        choice = input("\nDigite apenas o número: ").strip()

        # Permite escolher entre gerar novamente, salvar ou encerrar o fluxo.      
        if choice == "1":
            input_processed = False
            subject, grade, difficulty, theme = None, None, None, None
            subject, grade, difficulty, theme, input_processed, activity = process_input(subject, grade, difficulty, theme, input_processed, activity)

        elif choice == "2":
            print("\nReenviando prompt, aguarde...")
            subject, grade, difficulty, theme, input_processed, activity = process_input(subject, grade, difficulty, theme, input_processed, activity)

        elif choice == "3":
            if activity is None:
                print("\nNenhuma atividade gerada para salvar. Gere uma atividade primeiro.")
                continue
            else:
                print("\nSalvando atividade...")
                save_activity(activity)
                continue

        elif choice == "4":
            if from_library:
                print("\nVoltando para a biblioteca de atividades...")
                return

            print("\nIndo para a biblioteca de atividades...")
            menu_biblioteca()

        elif choice == "5":
            print("\nSaindo do módulo de geração de atividades...")
            return

        else:
            print("\nOpção inválida. Tente novamente.")
            continue


# Salva a atividade no banco de dados e trata possíveis erros.
def save_activity(activity):

    try:
        save_activity_to_database(activity)
        print("\nAtividade salva com sucesso na biblioteca!")

    except ValueError as e:
        print(f"{e}")


# ---------------------------------------------------------------
# 5) MENU DA BIBLIOTECA
# ---------------------------------------------------------------
def menu_biblioteca():
    # Regra 1: só usuário autenticado
    """
    if not usuario_autenticado:
        print("Acesso negado. Faça login para acessar a biblioteca.")
        return
    """
    try:
        atividades_salvas = carregar_atividades()
    except ValueError as e:
        print(f"\n{e}")
        return
    
    # Cenário 3: biblioteca vazia
    if len(atividades_salvas) == 0:
        print("\nVocê ainda não tem atividades salvas")
        resposta = input("\nDeseja ir ao gerador de atividades? (s/n): ").strip().lower()
        if resposta == "s":
            print("\nIndo para o gerador de atividades...")
            generate_activity(from_library=True)
            try:
                atividades_salvas = carregar_atividades()
            except ValueError as e:
                print(f"\n{e}")
                return

            if len(atividades_salvas) == 0:
                print("\nVocê ainda não tem atividades salvas")
                return
        else:
            print("\nVoltando para o menu principal...")
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
        escolha = input("\nEscolha: ").strip().lower()

        if escolha == "v":
            print("\nVoltando...")
            return
        elif escolha == "b":
            filtro = input("\nDigite o termo de busca: ").strip()
        elif escolha == "l":
            filtro = ""
        elif escolha.isdigit() and 1 <= int(escolha) <= len(resultado):
            quer_nova_impressao = exibir_atividade(resultado[int(escolha) - 1])
            if quer_nova_impressao:
                filtro = ""  # limpa o filtro e mostra a lista completa
                print("\nEscolha outra atividade para imprimir.")
        else:
            print("\nOpção inválida.")


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
        print(atividade["name"].upper())
        print(atividade["tag"])
        print(f"{atividade['description']} - {atividade['difficulty']}")
        print("=" * 50)
        print("Instruções:", atividade.get("instruction"))
        print("Gabarito:", atividade.get("answer"))
        print("Fontes:", atividade.get("resources"))

        print("\n[1] Imprimir   [0] Voltar à biblioteca")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            # Função da história IMP-01: gera o arquivo, mostra sucesso ou erro
            # e pergunta se o professor quer uma nova impressão.
            atividade_para_impressao = {
                "id": atividade["id"],
                "titulo": atividade["name"],
                "tag": atividade["tag"],
                "descrição": atividade["description"],
                "dificuldade": atividade["difficulty"],
                "enunciado": atividade.get("instruction"),
                "resposta": atividade.get("answer"),
                "fontes": atividade.get("resources")
            }
            quer_nova_impressao = imprimir_atividade(atividade_para_impressao)
            if quer_nova_impressao:
                return True
            # Se não quis (ou deu erro), a atividade continua na tela.
        elif opcao == "0":
            return False
        else:
            print("Opção inválida.")