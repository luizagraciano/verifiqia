from src.services.ai_integration import generate_activity_with_ai


# Solicita os parâmetros ao usuário e controla o fluxo de geração da atividade.
def process_input(subject, grade, difficulty, theme, input_processed):

    if not input_processed:
        while True:
            try:
                subject, grade, difficulty, theme = input("\nDigite o prompt com a disciplina, ano escolar, nível de dificuldade e tema, separados por vírgula, para gerar a atividade: ").split(",")
                subject, grade, difficulty, theme = subject.strip(), grade.strip(), difficulty.strip(), theme.strip()
                print("\nAguarde, gerando atividade...\n")
                break

            except ValueError:
                print("\nErro: Certifique-se de fornecer todos os parâmetros separados por vírgula.")

    try:
        # Gera a atividade e apresenta seus campos no terminal.
        activity = generate_activity_with_ai(subject, grade, difficulty, theme)

        print(activity['name'])
        print(activity['description'])
        print(activity['difficulty'])
        print(activity['instruction'])
        print(activity['answer'])
        print(activity['resources'])

        input_processed = True

    except ValueError as e:
        print(f"\nErro: {e}")

    return subject, grade, difficulty, theme, input_processed
    

# Exibe as opções disponíveis para continuar o fluxo da atividade.
def generate_activity():

    input_processed = False
    subject, grade, difficulty, theme = None, None, None, None

    print("\n============= Gerador de Atividades com IA =============")
    subject, grade, difficulty, theme, input_processed = process_input(subject, grade, difficulty, theme, input_processed)

    while True:
        print("\n=========== Menu de Geração de Atividade ===========")
        print("\nEscolha uma das opções abaixo para continuar:")
        print("[1] Gerar nova atividade")
        print("[2] Reenviar prompt")
        print("[3] Salvar atividade")
        print("[4] Sair")

        choice = input("\nDigite apenas o número: ").strip()

        # Permite escolher entre gerar novamente, salvar ou encerrar o fluxo.      
        if choice == "1":
            input_processed = False
            subject, grade, difficulty, theme = None, None, None, None
            subject, grade, difficulty, theme, input_processed = process_input(subject, grade, difficulty, theme, input_processed)

        elif choice == "2":
            print("\nReenviando prompt, aguarde...")
            subject, grade, difficulty, theme, input_processed = process_input(subject, grade, difficulty, theme, input_processed)

        elif choice == "3":
            print("\nSalvando atividade...")
            break # Provisório, pois a função de salvar ainda não foi implementada, remover em breve
            # Colocar função de salvar atividade aqui

        elif choice == "4":
            print("\nSaindo do programa...")
            break # Provisório, pois a função de menu principal ainda não foi implementada, remover em breve
            # Colocar função de menu principal aqui

        else:
            print("\nOpção inválida. Tente novamente.")
            continue