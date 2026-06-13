from typing import Optional

from pydantic import BaseModel, EmailStr


class FornecedorCreate(BaseModel):
    nome: str
    cnpj: str
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome": "Distribuidora ABC Ltda",
                "cnpj": "12.345.678/0001-90",
                "email": "contato@abc.com",
                "telefone": "(11) 98765-4321",
            }
        }
    }


class FornecedorResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    email: Optional[str] = None
    telefone: Optional[str] = None

    model_config = {"from_attributes": True}
