from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TipoMovimentacao(str, Enum):
    entrada = "entrada"
    saida = "saida"


class MovimentacaoCreate(BaseModel):
    produto_id: int
    tipo: TipoMovimentacao
    quantidade: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "produto_id": 1,
                "tipo": "entrada",
                "quantidade": 100,
            }
        }
    }


class MovimentacaoResponse(BaseModel):
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    data: datetime

    model_config = {"from_attributes": True}
