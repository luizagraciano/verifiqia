from src.services.offline import salvar_atividade_offline, listar_atividades_offline

print("--- TESTANDO SALVAR ---")
salvar_atividade_offline(
    name="Atividade de Teste", 
    description="Avaliando IA", 
    tag="Ética", 
    difficulty="Fácil",
    instruction="Verifique se o texto é verdadeiro.",
    answer="É falso.",
    resources="Nenhum."
)

print("\n--- TESTANDO LISTAR ---")
atividades = listar_atividades_offline()

# Verifica se a lista não está vazia antes de mostrar
if atividades:
    for atividade in atividades:
        print(dict(atividade)) 
else:
    print("Nenhuma atividade encontrada.")