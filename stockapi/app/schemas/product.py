from typing import Optional

from pydantic import BaseModel


class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int = 0
    fornecedor_id: Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome": "Caderno Universitário A4",
                "descricao": "Caderno universitário 200 folhas capa dura",
                "preco": 12.90,
                "quantidade": 50,
                "fornecedor_id": 1,
            }
        }
    }


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    quantidade: Optional[int] = None
    fornecedor_id: Optional[int] = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int
    fornecedor_id: Optional[int] = None

    model_config = {"from_attributes": True}
