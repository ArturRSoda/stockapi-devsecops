from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database import Base, engine

# importar todos os models antes do create_all para registrar as tabelas
from app.models import movement, product, supplier, user  # noqa: F401
from app.routers import auth, movements, products, suppliers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StockAPI",
    description="""
## API de Gestão de Estoque

Sistema para controle de inventário de pequenas empresas.

### Funcionalidades
- **Autenticação** — cadastro e login com JWT
- **Produtos** — controle completo do catálogo (busca, cadastro, edição, remoção)
- **Estoque** — registro de entradas e saídas com atualização automática de quantidade
- **Fornecedores** — cadastro e gestão de fornecedores

### Como usar
1. Crie um usuário em `POST /auth/register`
2. Faça login em `POST /auth/login` e copie o `access_token`
3. Clique em **Authorize** (cadeado) e cole o token para acessar os demais endpoints
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(movements.router)
app.include_router(suppliers.router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/redoc")
