# Verifiqia

## Descrição

O VerifiQIA é uma projeto desenvolvido para a disciplina de Projeto 1 da Cesar School no semestre de 2026.2. A aplicação é uma solução figital com foco no apoio ao desenvolvimento de atividades desplugadas voltadas para verificação de fatos, que trabalha o professor como mediador principal no processo de letramento em IA para alunos dos anos finais do Ensino Fundamental nas escolas públicas brasileiras. O projeto implementado funciona como um CRUD simples, rodado em linha de comando, e funciona como MVP da proposta de solução elaborada.

## Tecnologias utilizadas

- **Python**: linguagem principal do projeto.
- **Click**: criação da interface de linha de comando.
- **SQLite**: banco de dados local e arquivo `data/database.sqlite`.
- **bcrypt**: geração de hashes seguros para senhas.
- **Google GenAI**: dependências preparadas para integração com recursos de
  inteligência artificial.
- **pytest**: execução dos testes automatizados.
- **python-dotenv**: suporte à configuração por variáveis de ambiente.

## Estrutura do repositório

```text
verifiqia/
├── data/
│   └── database.sqlite       # Banco de dados local
├── src/
│   ├── database/
│   │   ├── connection.py     # Conexão e preparação do banco
│   │   ├── schema.sql        # Estrutura das tabelas
│   │   ├── seed.sql          # Dados iniciais
│   │   └── __init__.py
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
│   └── test_storage.py       # Testes de persistência
├── .env.example              # Modelo de variáveis de ambiente
├── main.py                   # Ponto de entrada da CLI
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

```powershell
Copy-Item .env.example .env
```

### 5. Inicializar e preparar o banco de dados

```powershell
python main.py init-db
python main.py seed-db
```

O primeiro comando cria as tabelas definidas em `src/database/schema.sql`. O
segundo carrega os dados iniciais definidos em `src/database/seed.sql`.

### 6. Executar os testes

```powershell
python -m pytest
```

### 7. Consultar os comandos disponíveis

```powershell
python main.py --help
```