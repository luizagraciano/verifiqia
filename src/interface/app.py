from src.services.exporter import imprimir_atividade
from src.services.activity import save_activity_to_database, edit_activity_in_database, delete_activity_in_database
from src.services.ai_integration import generate_activity_with_ai
from src.services.library import (
    buscar_atividades,
    carregar_atividade,
    carregar_atividades
)


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


# Edita a ativid
def edit_activity(activity_id):
    
    name, description, tag, difficulty, instruction, answer, resources = None, None, None, None, None, None, None

    while True:
        print("\n========== Menu de Edição de Atividade ==========")
        print("\nEscolha uma das opções abaixo para continuar:")
        print("[1] Editar título")
        print("[2] Editar descrição")
        print("[3] Editar instrução")
        print("[4] Editar resposta")
        print("[5] Editar fontes")
        print("[6] Editar dificuldade")
        print("[7] Editar tag")
        print("[8] Sair do módulo de edição de atividades")
    
        choice = input("\nDigite apenas o número: ").strip()
    
        # Permite escolher qual campo editar ou encerrar o fluxo.      
        if choice == "1":
            name = input("\nDigite o novo título da atividade: ").strip()

            if not name:
                print("\nTítulo inválido. Por favor, insira um título válido.")
                continue
            else:
                process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources)

        elif choice == "2":
            description = input("\nDigite a nova descrição da atividade: ").strip()

            if not description:
                print("\nDescrição inválida. Por favor, insira uma descrição válida.")
                continue
            else:
                process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources)

        elif choice == "3":
            instruction = input("\nDigite a nova instrução da atividade: ").strip()
            
            if not instruction:
                print("\nInstrução inválida. Por favor, insira uma instrução válida.")
                continue
            else:
                process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources)

        elif choice == "4":
            answer = input("\nDigite a nova resposta da atividade: ").strip()

            if not answer:
                print("\nResposta inválida. Por favor, insira uma resposta válida.")
                continue
            else:
                process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources)

        elif choice == "5":
            resources = input("\nDigite as novas fontes da atividade: ").strip()
            
            if not resources:
                print("\nFontes inválidas. Por favor, insira fontes válidas.")
                continue
            else:
                process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources)

        elif choice == "6":
            difficulty = input("\nDigite a nova dificuldade da atividade: ").strip()
            
            if not difficulty:
                print("\nDificuldade inválida. Por favor, insira uma dificuldade válida.")
                continue
            else:
                process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources)

        elif choice == "7":
            tag = input("\nDigite a nova tag da atividade: ").strip()
            if not tag:
                print("\nTag inválida. Por favor, insira uma tag válida.")
                continue
            else:
                process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources)

        elif choice == "8":
            print("\nSaindo do módulo de edição de atividades...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")
            continue


def process_activity_update(activity_id, name, description, tag, difficulty, instruction, answer, resources):

    try:
        print("\nEditando atividade...")
        updated_activity = edit_activity_in_database(activity_id, name, description, tag, difficulty, instruction, answer, resources)
        display_updated_activity(updated_activity)
    except ValueError as e:
        print(f"{e}")


def display_updated_activity(updated_activity):
    
    print(updated_activity['name'])
    print(updated_activity['tag'])
    print(updated_activity['description'])
    print(updated_activity['difficulty'])
    print(updated_activity['instruction'])
    print(updated_activity['answer'])
    print(updated_activity['resources'])


def delete_activity(activity_id):

    while True:
        print("\nTem certeza que deseja excluir a atividade?")
        print("[1] Sim, excluir a atividade")
        print("[2] Não, voltar ao menu anterior")

        choice = input("\nDigite apenas o número: ").strip()

        if choice == "1":
            try:
                print("\nDeletando atividade...")
                delete_activity_in_database(activity_id)
                print("\nAtividade deletada com sucesso da biblioteca!")
            except ValueError as e:
                print(f"{e}")
            break
        elif choice == "2":
            print("\nExclusão cancelada. Voltando ao menu anterior...")
            break
        else:
            print("\nOpção inválida. Por favor, digite 's' para sim ou 'n' para não.")
            continue


# ---------------------------------------------------------------
# 5) MENU DA BIBLIOTECA
# ---------------------------------------------------------------
def obter_atividades_salvas():
    try:
        return carregar_atividades()
    except ValueError as e:
        print(f"\n{e}")
        return None


def menu_biblioteca():
    # Regra 1: só usuário autenticado
    """
    if not usuario_autenticado:
        print("Acesso negado. Faça login para acessar a biblioteca.")
        return
    """
    atividades_salvas = obter_atividades_salvas()
    if atividades_salvas is None:
        return
    
    # Cenário 3: biblioteca vazia
    if len(atividades_salvas) == 0:
        print("\nVocê ainda não tem atividades salvas")
        resposta = input("\nDeseja ir ao gerador de atividades? (s/n): ").strip().lower()
        if resposta == "s":
            print("\nIndo para o gerador de atividades...")
            generate_activity(from_library=True)
            atividades_salvas = obter_atividades_salvas()
            if atividades_salvas is None:
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
            atividade_resumida = resultado[int(escolha) - 1]
            try:
                atividade = carregar_atividade(atividade_resumida["id"])
            except ValueError as e:
                print(f"\n{e}")
                continue

            iniciar_nova_impressao = exibir_atividade(atividade)

            if iniciar_nova_impressao:
                filtro = ""
                print("\nEscolha outra atividade para imprimir.")

            atividades_salvas = obter_atividades_salvas()
            if atividades_salvas is None:
                return
        else:
            print("\nOpção inválida.")


def listar_atividades(lista):
    print("\n============ Biblioteca de Atividades ============\n")
    if len(lista) == 0:
        print("Nenhuma atividade encontrada")
        return
    for numero, atividade in enumerate(lista, start=1):
        print(
            f"[{numero}] {atividade['name']} "
            f"({atividade['description']}, {atividade['difficulty']}, {atividade['tag'] or 'Sem tag'})"
        )


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
        print(atividade["tag"] or "Sem tag")
        print(f"{atividade['description']} - {atividade['difficulty']}")
        print("=" * 50)
        print("Instruções:", atividade["description"])
        print("Gabarito:", atividade["answer"])
        print("Fontes:", atividade["resources"])
        print("\nEscolha uma das opções abaixo para continuar:")
        print("[1] Imprimir")
        print("[2] Editar atividade")
        print("[3] Excluir atividade")
        print("[4] Voltar à biblioteca")
        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            # Função da história IMP-01: gera o arquivo, mostra sucesso ou erro
            # e pergunta se o professor quer uma nova impressão.
            atividade_para_impressao = {
                "id": atividade["id"],
                "titulo": atividade["name"],
                "objetivo": atividade["description"],
                "dificuldade": atividade["difficulty"],
                "enunciado": atividade.get("instruction"),
                "resposta": atividade.get("answer"),
                "fontes": atividade.get("resources")
            }

            try:
                documento_gerado = imprimir_atividade(atividade_para_impressao)
                print("\nDocumento gerado com sucesso!")
                print(f"\nArquivo: {documento_gerado}")

                if perguntar_nova_impressao():
                    return True
                
            except Exception as e:
                print(f"{e}")
                
            # Se não quis (ou deu erro), a atividade continua na tela.
        elif opcao == "2":
            edit_activity(atividade["id"])
            try:
                atividade = carregar_atividade(atividade["id"])
            except ValueError as e:
                print(f"\n{e}")
                return False
        elif opcao == "3":
            delete_activity(atividade["id"])
            try:
                atividade = carregar_atividade(atividade["id"])
            except ValueError as e:
                print(f"\n{e}")
                return False
        elif opcao == "4":
            return False
        else:
            print("Opção inválida.")


def perguntar_nova_impressao():
    while True:
        print("\nO que deseja fazer agora?")
        print("[1] Iniciar uma nova impressão")
        print("[2] Voltar à tela da atividade")
        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            return True
        elif opcao == "2":
            return False
        else:
            print("Opção inválida.")