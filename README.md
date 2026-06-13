# StockAPI + Pipeline DevSecOps

API REST de gestão de estoque desenvolvida com FastAPI e PostgreSQL, com pipeline
DevSecOps completo integrado ao GitHub Actions. O projeto foi construído como
trabalho prático da disciplina **INE5429 - Segurança em Computação** (UFSC),
cobrindo as cinco categorias de análise de segurança: Secret Detection, SCA, SAST,
IaC Scanning e DAST.

---

## Stack

| Camada        | Tecnologia                              |
|---------------|-----------------------------------------|
| API           | FastAPI 0.111, Python 3.11              |
| ORM           | SQLAlchemy 2.x                          |
| Banco de dados| PostgreSQL 15                           |
| Autenticação  | JWT (PyJWT 2.8.0) + bcrypt              |
| Container     | Docker + Docker Compose                 |
| IaC           | Terraform (AWS S3)                      |
| CI/CD         | GitHub Actions                          |

---

## Pipeline de Segurança

O pipeline é disparado em todo push e pull request. Os cinco jobs rodam em paralelo
com `continue-on-error: true`, garantindo que todos completem mesmo quando há
findings.

| Job                        | Ferramenta     | O que analisa                                |
|----------------------------|----------------|----------------------------------------------|
| Secret Detection           | Gitleaks 8.18  | Segredos e credenciais nos arquivos           |
| SCA                        | pip-audit       | CVEs nas dependências Python                 |
| SAST                       | Bandit          | Padrões inseguros no código-fonte            |
| IaC Scan                   | Checkov 3.x     | Dockerfile, Docker Compose e Terraform       |
| DAST                       | OWASP ZAP       | Vulnerabilidades na aplicação em execução    |

Os relatórios de cada ferramenta são salvos como artefatos no GitHub Actions
(`sca-report.json`, `sast-report.json`, `iac-report.json`, `zap-report`).

---

## Funcionalidades da API

- **Autenticação** com registro e login via JWT Bearer Token
- **Produtos** com CRUD completo e busca por nome (case-insensitive)
- **Movimentações de estoque** com atualização automática de quantidade
- **Fornecedores** com cadastro e listagem

A documentação interativa fica disponível em `/docs` (Swagger UI) ou `/redoc`
após subir a aplicação.

---

## Como rodar localmente

**Pré-requisitos:** Docker e Docker Compose instalados.

```bash
# 1. Clone o repositório
git clone https://github.com/ArturRSoda/TrabalhoDevSecOps.git
cd TrabalhoDevSecOps/stockapi

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com os valores desejados para SECRET_KEY e senha do banco

# 3. Suba a aplicação
docker compose up --build

# 4. Acesse
# Documentação: http://localhost:8000/docs
# Redoc:        http://localhost:8000/redoc
```

---

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha antes de rodar:

| Variável        | Descrição                                   |
|-----------------|---------------------------------------------|
| `SECRET_KEY`    | Chave usada para assinar os tokens JWT      |
| `DATABASE_URL`  | URL de conexão com o PostgreSQL             |
| `POSTGRES_USER` | Usuário do banco                            |
| `POSTGRES_PASSWORD` | Senha do banco                          |
| `POSTGRES_DB`   | Nome do banco de dados                      |

O arquivo `.env` está no `.gitignore` e nunca deve ser commitado.

---

## Estrutura do repositório

```
.
├── .github/workflows/devsecops.yml   # Pipeline de segurança
├── .gitleaks.toml                    # Regras customizadas do Gitleaks
├── stockapi/
│   ├── app/
│   │   ├── config.py                 # Configurações (lê SECRET_KEY do ambiente)
│   │   ├── database.py
│   │   ├── dependencies.py           # Injeção de dependências (auth)
│   │   ├── models/                   # Modelos SQLAlchemy
│   │   ├── routers/                  # Endpoints (auth, products, movements, suppliers)
│   │   └── schemas/                  # Schemas Pydantic
│   ├── tests/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
└── terraform/
    └── main.tf                       # Bucket S3 para backup do inventário
```

---

## Contexto acadêmico

Trabalho prático individual da disciplina **INE5429 - Segurança em Computação**,
Universidade Federal de Santa Catarina.

Professores: Jean Everson Martina / Thaís Bardini Idalino.
