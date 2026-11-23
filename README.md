# Verifiqia

## Descrição

O VerifiQIA é uma projeto desenvolvido para a disciplina de Projeto 1 da Cesar School no semestre de 2026.2. A aplicação é uma solução figital com foco no apoio ao desenvolvimento de atividades desplugadas voltadas para verificação de fatos, que trabalha o professor como mediador principal no processo de letramento em IA para alunos dos anos finais do Ensino Fundamental nas escolas públicas brasileiras. O projeto implementado funciona como um CRUD simples, rodado em linha de comando, e funciona como MVP da proposta de solução elaborada.

## Tecnologias utilizadas

- **Python 3.14**: linguagem principal do projeto.
- **Click**: criação da interface de linha de comando.
- **SQLite**: banco de dados local e arquivo `data/database.sqlite`.
- **bcrypt**: geração de hashes seguros para senhas.
- **validate-docbr**: validação de CPF
- **Google GenAI**: dependências preparadas para integração com recursos de inteligência artificial.
- **pytest**: execução dos testes automatizados.
- **python-dotenv**: suporte à configuração por variáveis de ambiente.

## Estrutura do repositório

```text
verifiqia/
├── src/
│   ├── database/
│   │   ├── connection.py     # Conexão e preparação do banco
│   │   ├── schema.sql        # Estrutura das tabelas
│   │   ├── seed.sql          # Dados iniciais
│   │   └── storage.py        # Operações de persistência
│   ├── interface/
│   │   └── app.py            # Camada de interface da aplicação
│   └── services/
│       ├── activity.py       # Serviços relacionados às atividades
│       ├── ai_integration.py # Integração com inteligência artificial
│       ├── auth.py           # Operações de autenticação e senhas
│       ├── exporter.py       # Exportação de dados
│       ├── library.py        # Operações da biblioteca
│       └── offline.py         # Recursos para uso offline
├── tests/
│   ├── conftest.py           # Fixtures e configuração dos testes
│   ├── test_activity.py      # Testes das atividades
│   └── test_storage.py       # Testes de persistência
├── utilities/
│   └── cli.py                # Inicialização e execução auxiliar do sistema
├── .env.example              # Modelo de variáveis de ambiente
├── .gitignore
├── main.py                   # Inicializa o banco e inicia a aplicação
├── requirements.txt          # Dependências do projeto
└── README.md
```

## Como rodar o projeto

### 1. Clonar e acessar o repositório

```powershell
git clone https://github.com/luizagraciano/verifiqia.git
cd verifiqia
```

### 2. Criar e ativar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação de scripts, execute o terminal como
usuário apropriado ou use diretamente o executável do ambiente virtual nos
comandos seguintes.

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Se a integração com a API do Gemini for utilizada, copie o arquivo de
exemplo e preencha a variável GEMINI_API_KEY com a sua chave de API obtida no Google AI Studio:
https://aistudio.google.com/api-keys

```powershell
Copy-Item .env.example .env
```

#### Simulação do estado de conexão

A variável `CONNECTION_STATUS`, localizada no arquivo `.env`, define o modo
de conexão usado pela aplicação:

- `CONNECTION_STATUS="online"`: inicia normalmente e permite usar os recursos
  de geração de atividades com IA.
- `CONNECTION_STATUS="offline"`: inicia em modo offline, bloqueia o acesso
  ao gerador de atividades e permite usar o banco de atividades pré-carregado.

Atenção: esta configuração simula o estado da conexão e não verifica se o
dispositivo está realmente conectado à internet. Você pode modificar o valor
em tempo de execução para ver como a aplicação responde ao estado online/offline.

### 5. Iniciar o programa

O `main.py` é o ponto de entrada recomendado. Ao executá-lo, a aplicação
cria o banco, executa o seed e inicia a interface interativa automaticamente:

```powershell
python -m main
```

O arquivo `main.py` realiza, nesta ordem:

1. `init_db()`: cria as tabelas a partir de `src/database/schema.sql`.
2. `seed_db()`: carrega os dados iniciais de `src/database/seed.sql`.
3. `init_app()`: inicia o programa.

O banco SQLite é criado em `data/database.sqlite`, por isso não é necessário
executar a inicialização manual antes de usar `main.py`.

Como alternativa, os comandos da CLI podem ser usados separadamente:

```powershell
python utilities/cli.py init-db
python utilities/cli.py seed-db
python utilities/cli.py init-app
```

### 6. Executar os testes automatizados

```powershell
python -m pytest
```

### 7. Consultar os comandos disponíveis para testes individualizados

```powershell
python utilities/cli.py --help
```