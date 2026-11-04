from src.services.activity import save_activity_to_database
from src.services.ai_integration import generate_activity_with_ai


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
            # Colocar função de biblioteca de atividades aqui
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
def generate_activity():

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
            print("\nIndo para a biblioteca de atividades...")
            # Colocar função de biblioteca de atividades aqui

        elif choice == "5":
            print("\nSaindo do módulo de geração de atividades...")
            break # Provisório, pois a função de menu principal ainda não foi implementada, remover em breve
            # Colocar função de menu principal aqui

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
