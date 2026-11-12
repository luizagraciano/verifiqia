import os  # biblioteca padrão do Python para trabalhar com pastas

# Pasta onde os documentos serão salvos
PASTA_SAIDA = "saida"

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
    linhas.append("DIFICULDADE")
    linhas.append(atividade["dificuldade"])
    linhas.append("")
    linhas.append("ENUNCIADO")
    linhas.append(atividade["enunciado"])
    linhas.append("")
    linhas.append("GABARITO")
    linhas.append(atividade["resposta"])
    linhas.append("")
    linhas.append("FONTES")
    linhas.append(atividade["fontes"])
    linhas.append("")
    linhas.append("-" * 60)
    linhas.append("Gerado pelo VerifiQIA")
    return "\n".join(linhas)


# ---------------------------------------------------------------
# 2) GERAR O ARQUIVO (Cenários 1 e 2 dos critérios de aceite)
# Funciona 100% offline: só grava um arquivo no computador.
# Devolve True se deu certo e False se deu erro.
# ---------------------------------------------------------------
def imprimir_atividade(atividade):
    try:
        os.makedirs(PASTA_SAIDA, exist_ok=True)  # cria a pasta se não existir
        caminho = os.path.join(PASTA_SAIDA, f"atividade_{atividade['id']}.txt")

        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(montar_documento(atividade))
        return os.path.abspath(caminho)
    
    except OSError:
        # Cenário 2: falha (pasta sem permissão, disco cheio...)
        raise ValueError("\nNão foi possível gerar o documento. "
              "Verifique o local de gravação e tente novamente.")
