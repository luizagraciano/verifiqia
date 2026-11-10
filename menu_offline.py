from src.services.offline import TAGS_SISTEMA, salvar_atividade_offline, buscar_atividades_por_tag_offline

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
            print("Número de tag inválido.")
            return None
    except ValueError:
        print("Erro: Por favor, digite apenas o NÚMERO.")
        return None

def rodar_menu_offline():
    while True:
        print("\n=== BIBLIOTECA OFFLINE (TESTE) ===")
        print("1. Salvar nova atividade de teste")
        print("2. Filtrar atividades por Tag")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n--- SALVAR ATIVIDADE ---")
            tag_escolhida = escolher_tag("Digite o número da tag para esta atividade: ")
            
            if tag_escolhida:
                try:
                    # Salva a atividade com a tag que o usuário escolheu
                    salvar_atividade_offline(
                        name=f"Atividade de {tag_escolhida}", 
                        description="Teste de Filtro", 
                        tag=tag_escolhida, 
                        difficulty="Fácil",
                        instruction="Verifique se o texto é verdadeiro.",
                        answer="É falso.",
                        resources="Nenhum."
                    )
                    print(f"Sucesso! Atividade de {tag_escolhida} salva no banco.")
                except Exception as e:
                    print(f"Erro ao salvar: {e}")

        elif opcao == '2':
            print("\n--- FILTRAR ATIVIDADES ---")
            tag_escolhida = escolher_tag("Digite o número da tag para buscar: ")
            
            if tag_escolhida:
                print(f"\nBuscando atividades de {tag_escolhida}...")
                try:
                    resultados = buscar_atividades_por_tag_offline(tag_escolhida)
                    
                    if resultados:
                        print(f"Encontramos {len(resultados)} atividade(s):")
                        for atv in resultados:
                            print(f"- ID: {atv['id']} | Nome: {atv['name']} | Tag: {atv['tag']}")
                    else:
                        print(f"Nenhuma atividade encontrada com a tag '{tag_escolhida}'.")
                except Exception as e:
                    print(f"Erro ao buscar no banco: {e}")
                
        elif opcao == '3':
            print("Saindo do menu de teste...")
            break
        else:
            print("Opção inválida. Digite 1, 2 ou 3.")

if __name__ == "__main__":
    rodar_menu_offline()