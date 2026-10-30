from src.services.ai_integration import generate_activity_with_ai

# Solicita os parâmetros ao usuário e controla o fluxo de geração da atividade.
def generate_activity():

    try:
        # Lê e normaliza os quatro parâmetros exigidos pelo gerador de IA.
        subject, grade, difficulty, theme = input("Digite o prompt com a disciplina, ano escolar, nível de dificuldade e tema, separados por vírgula, para gerar a atividade: ").split(",")
        subject, grade, difficulty, theme = subject.strip(), grade.strip(), difficulty.strip(), theme.strip()
    except ValueError:
        print("Erro: Certifique-se de fornecer todos os parâmetros separados por vírgula.")
        return
    
    while True:
        try:
            # Gera a atividade e apresenta seus campos no terminal.
            print("Aguarde, gerando atividade...")
            activity = generate_activity_with_ai(subject, grade, difficulty, theme)
            print(activity['name'])
            print(activity['description'])
            print(activity['difficulty'])
            print(activity['instruction'])
            print(activity['answer'])
            print(activity['resources'])
        except ValueError as e:
            print(f"{e}")

        # Permite escolher entre gerar novamente, salvar ou encerrar o fluxo.
        choice = menu_activity()

        if choice == "1":
            return
        elif choice == "2":
            print("Reenviando prompt...")
            continue
        elif choice == "3":
            print("Salvando atividade...")
            break
        elif choice == "4":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            choice = menu_activity()

# Exibe as opções disponíveis para continuar o fluxo da atividade.
def menu_activity():
    while True:
        print("=== Menu ===")
        print("1. Gerar nova atividade")
        print("2. Reenviar prompt")
        print("3. Salvar atividade")
        print("4. Sair")
        choice = input("Escolha uma opção, digite apenas o número: ")
        return choice