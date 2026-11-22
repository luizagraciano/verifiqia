import os
from dotenv import load_dotenv
from getpass import getpass
from validate_docbr import CPF
from src.services.auth import check_login, register_user
from src.services.exporter import imprimir_atividade
from src.services.activity import save_activity_to_database, edit_activity_in_database, delete_activity_in_database
from src.services.ai_integration import generate_activity_with_ai
from src.services.offline import TAGS_SISTEMA, carregar_atividade_offline, listar_atividades_offline, buscar_atividades_por_tag_offline
from src.services.library import (
    buscar_atividades,
    carregar_atividade,
    carregar_atividades
)


def init_app():
    while True:
        load_dotenv(override=True)  # Carrega variáveis de ambiente do arquivo .env

        app_mode = os.environ.get("CONNECTION_STATUS")

        if app_mode == "offline":
            print("\n=================== VerifiQIA ===================")
            print("\nVocê está sem conexão com a internet. Conecte-se para iniciar o uso da aplicação.")
            refresh = input("\nDeseja tentar novamente? (s/n): ").strip().lower()
            if refresh == "s":
                continue
            else:
                print("\nSaindo da aplicação...")
                exit()
        else:
            break  # Sai do loop se a conexão estiver ativa

    while True:
        print("\n=================== VerifiQIA ===================")
        print("\nTem uma conta? Faça login ou cadastre-se para continuar.")
        print("\n[1] Login")
        print("[2] Cadastro")
        choice = input("\nDigite apenas o número: ").strip()

        if choice == "1":
            login()
        elif choice == "2":
            register()
        else:
            print("\nOpção inválida. Tente novamente.")
            continue


def login():
    logged_user = None

    print("\n===================== Login =====================")
 
    for attempt in range(3):
        login_email = input("\nE-mail: ").strip().lower()
        login_password = getpass(prompt="\nSenha: ", echo_char="*")
 
        try:
            logged_user = check_login(login_email, login_password)
            break
        except ValueError as e:
            print(f"{e}")
            answer = input("\nQuer realizar o cadastro? (s/n): ").strip().lower()
            if answer == "s":
                register()
                return  # Sai da função login após o cadastro

    if logged_user is not None:
        print(f"\nBem-vindo(a), {logged_user['username'].split()[0]}!")
        main_menu()
    else:
        print("\nVocê excedeu o número máximo de tentativas. Tente novamente mais tarde ou faça o cadastro.")


def register():
    print("\n============= Cadastro de Professor =============")
 
    # Nome e sobrenome, sem números
    while True:
        name = " ".join(input("\nNome completo: ").split())  # tira espaços extras
        if len(name.split()) >= 2 and not any(c.isdigit() for c in name):
            break
        print("\nNome inválido. Digite nome e sobrenome, sem números.")
 
    # E-mail: um "@", sem espaços, e um ponto no domínio (ex.: nome@escola.com)
    while True:
        email = input("\nE-mail: ").strip().lower()
        if email.count("@") == 1 and " " not in email:
            local, domain = email.split("@")
            if local != "" and "." in domain and not domain.startswith(".") and not domain.endswith("."):
                break
        print("\nE-mail inválido. Exemplo: nome@escola.com")
 
    # CPF: 11 dígitos, validado com o módulo validate-docbr
    while True:
        cpf = input("\nCPF: ").strip()
        if CPF().validate(cpf):
            break
        print("\nCPF inválido. Digite um CPF válido.")

    # Senha: mínimo 8 caracteres, com letras e números, digitada duas vezes
    while True:
        password = getpass(prompt="\nSenha (mín. 8 caracteres, com letras e números): ", echo_char="*")
 
        if len(password) < 8 or not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            print("\nSenha inválida. Use pelo menos 8 caracteres, com letras e números.")
            continue
 
        if password != getpass(prompt="\nConfirme a senha: ", echo_char="*"):
            print("\nAs senhas não conferem. Digite novamente.")
            continue
 
        break

    try:
        register_user(name, email, cpf, password)
        print("\nCadastro realizado com sucesso! Faça login para continuar.")
        login()  # Chama a função de login após o cadastro bem-sucedido
    except ValueError as e:
        print(f"\nErro ao cadastrar usuário: {e}")


# Exibe o menu principal da aplicação e direciona para os fluxos de geração de atividades ou biblioteca de atividades.
def main_menu():

    while True:
        print("\n=================== VerifiQIA ===================")
        print("\n================= Menu Principal =================")
        print("\nEscolha uma das opções abaixo para continuar:")
        print("[1] Gerar atividade com inteligência artificial")
        print("[2] Biblioteca de Atividades")
        print("[3] Banco de Atividades Offline")
        print("[4] Sair")

        choice = input("\nDigite apenas o número: ").strip()

        if choice == "1":
            generate_activity()
        elif choice == "2":
            print("\nIndo para a biblioteca de atividades...")
            menu_biblioteca()
        elif choice == "3":
            print("\nIndo para o banco de atividades offline...")
            rodar_menu_offline()
        elif choice == "4":
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
    while True:
        load_dotenv(override=True)  # Carrega variáveis de ambiente do arquivo .env
    
        app_mode = os.getenv("CONNECTION_STATUS")
    
        if app_mode == "offline":
            print("\nVocê está no modo offline. A geração de atividades com IA não está disponível.")
            print("[1] Acessar o Banco de Atividades Offline")
            print("[2] Recarregar a conexão com a internet para usar o gerador de atividades com IA.")
            print("[3] Voltar")
            choice = input("\nEscolha uma opção: ").strip()
            if choice == "1":
                rodar_menu_offline()
            elif choice == "2":
                print("\nRecarregando a conexão...")
                continue
            else:
                print("\nVoltando...")
                return
        else:
            break  # Sai do loop se a conexão estiver ativa
    
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
                "enunciado": atividade["instruction"],
                "resposta": atividade["answer"],
                "fontes": atividade["resources"]
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


def escolher_tag(mensagem_prompt: str):
    """Função auxiliar para mostrar as tags e retornar a escolhida."""
    print("\n--- TAGS DISPONÍVEIS ---")
    for i, tag in enumerate(TAGS_SISTEMA, start=1):
        print(f"{i}. {tag}")
    
    try:
        escolha = int(input(mensagem_prompt)) - 1
        if 0 <= escolha < len(TAGS_SISTEMA):
            return TAGS_SISTEMA[escolha]
        else:
            print("\nNúmero de tag inválido.")
            return None
    except ValueError:
        print("\nErro: Por favor, digite apenas o NÚMERO.")
        return None


def rodar_menu_offline():
    while True:
        print("\n=========== Banco de Atividades Offline ===========")
        atividades_offline = listar_atividades_offline()
        lista_offline = exibir_atividades_offline(atividades_offline) # Exemplo: busca atividades de uma tag específica

        print("\n[F] Filtrar atividades por tag")
        print("[V] Voltar")
        opcao = input("\nDigite o número da atividade para ver detalhes, ou escolha uma opção: ").strip().upper()

        if opcao.isdigit() and 1 <= int(opcao) <= len(lista_offline):
            atividade_resumida = lista_offline[int(opcao) - 1]
            try:
                atividade = carregar_atividade_offline(atividade_resumida["id"])
                exibir_detalhes_atividade(atividade)
            except ValueError as e:
                print(f"\n{e}")
                continue

        elif opcao == "F":
            print("\n--- FILTRAR ATIVIDADES ---")
            tag_escolhida = escolher_tag("\nDigite o número da tag para buscar: ")
            
            if tag_escolhida:
                print(f"\nBuscando atividades de {tag_escolhida}...")
                try:
                    resultados = buscar_atividades_por_tag_offline(tag_escolhida)
                    
                    if resultados:
                        print(f"\nEncontramos {len(resultados)} atividade(s):")
                        exibir_atividades_offline(resultados)
                    else:
                        print(f"\nNenhuma atividade encontrada com a tag '{tag_escolhida}'.")
                except Exception as e:
                    print(f"{e}")
                
        elif opcao == "V":
            print("\nVoltando...")
            return
        else:
            print("\nOpção inválida. Tente novamente.")


def exibir_atividades_offline(atividades_offline):
    for numero, atividade in enumerate(atividades_offline, start=1):
        print(
            f"[{numero}] {atividade['name']} "
            f"({atividade['description']}, {atividade['difficulty']}, {atividade['tag'] or 'Sem tag'})"
        )
    return atividades_offline


def exibir_detalhes_atividade(atividade):
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
        print("[1] Salvar na Biblioteca")
        print("[2] Voltar")
        opcao = input("\nEscolha: ").strip()

        if opcao == '1':
            try:
                save_activity_to_database(atividade)
                print("\nAtividade salva com sucesso na biblioteca!")
        
            except ValueError as e:
                print(f"{e}")
        elif opcao == '2':
            return
        else:
            print("\nOpção inválida. Tente novamente.")
            continue
