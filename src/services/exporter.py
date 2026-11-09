"""
VerifiQIA - História IMP-01: Gerar documento imprimível a partir de uma atividade

Este arquivo funciona de duas formas:
  1) Importado pela biblioteca (biblioteca_atividades.py), que usa a função imprimir_atividade().
  2) Sozinho, para testar:  python imprimir_atividade.py

"""

import os  # biblioteca padrão do Python para trabalhar com pastas

# Pasta onde os documentos serão salvos
PASTA_SAIDA = "saida"

# Atividade de exemplo, usada só quando este arquivo roda sozinho.
atividade_exemplo = {
    "id": 1,
    "titulo": "Detetives de Notícias",
    "objetivo": "Ensinar os alunos a identificar sinais de alerta em textos gerados por IA.",
    "enunciado": "Em grupos, analisem três textos curtos e decidam quais parecem confiáveis.",
    "passo_a_passo": [
        "Divida a turma em grupos de 4 alunos.",
        "Entregue três textos impressos para cada grupo.",
        "Cada grupo apresenta sua conclusão em 2 minutos.",
    ],
}


# ---------------------------------------------------------------
# 1) MONTAR O TEXTO DO DOCUMENTO (layout de impressão)
# Regra 3: só título, objetivo, enunciado e passo a passo (sem dados de alunos).
# ---------------------------------------------------------------
def montar_documento(atividade):
    linhas = []
    linhas.append("=" * 60)
    linhas.append(atividade["titulo"].upper())
    linhas.append("=" * 60)
    linhas.append("")
    linhas.append("OBJETIVO / ORIENTAÇÕES AO PROFESSOR")
    linhas.append(atividade["objetivo"])
    linhas.append("")
    linhas.append("ENUNCIADO")
    linhas.append(atividade["enunciado"])
    linhas.append("")
    linhas.append("PASSO A PASSO")
    for numero, passo in enumerate(atividade["passo_a_passo"], start=1):
        linhas.append(f"{numero}. {passo}")
    linhas.append("")
    linhas.append("-" * 60)
    linhas.append("Gerado pelo VerifiQIA")
    return "\n".join(linhas)


# ---------------------------------------------------------------
# 2) GERAR O ARQUIVO (Cenários 1 e 2 dos critérios de aceite)
# Funciona 100% offline: só grava um arquivo no computador.
# Devolve True se deu certo e False se deu erro.
# ---------------------------------------------------------------
def gerar_documento(atividade):
    try:
        os.makedirs(PASTA_SAIDA, exist_ok=True)  # cria a pasta se não existir
        caminho = os.path.join(PASTA_SAIDA, f"atividade_{atividade['id']}.txt")

        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(montar_documento(atividade))

        # Cenário 1: sucesso
        print("\nDocumento gerado com sucesso!")
        print("Arquivo:", os.path.abspath(caminho))
        return True

    except OSError:
        # Cenário 2: falha (pasta sem permissão, disco cheio...)
        print("\nNão foi possível gerar o documento. "
              "Verifique o local de gravação e tente novamente.")
        return False


# ---------------------------------------------------------------
# 3) PERGUNTAR O QUE FAZER DEPOIS DE IMPRIMIR
# Devolve True se o professor quer iniciar uma nova impressão.
# ---------------------------------------------------------------
def perguntar_nova_impressao():
    while True:
        print("\nO que deseja fazer agora?")
        print("[1] Iniciar uma nova impressão")
        print("[0] Voltar à tela da atividade")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            return True
        elif opcao == "0":
            return False
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------
# 4) FUNÇÃO PRINCIPAL DA IMPRESSÃO (é a que a biblioteca chama)
# Gera o documento. Se deu certo, mostra a mensagem de sucesso e
# pergunta se quer uma nova impressão.
# Devolve True se quer nova impressão; False se quer ficar na atividade.
# Se deu erro, não pergunta nada: a atividade continua na tela.
# ---------------------------------------------------------------
def imprimir_atividade(atividade):
    if gerar_documento(atividade):
        return perguntar_nova_impressao()
    return False


# ---------------------------------------------------------------
# 5) TESTE ISOLADO
# Só roda se você executar ESTE arquivo diretamente.
# Quando o arquivo é importado, esta parte é ignorada.
# ---------------------------------------------------------------
def main():
    while True:
        print("\n" + "=" * 50)
        print(atividade_exemplo["titulo"].upper())
        print("=" * 50)
        print("\n[1] Imprimir   [0] Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            if imprimir_atividade(atividade_exemplo):
                print("\nNova impressão: na biblioteca, você escolheria outra atividade.")
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
