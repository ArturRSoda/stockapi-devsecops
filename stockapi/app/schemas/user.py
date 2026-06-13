from enum import Enum
from pydantic import BaseModel, EmailStr


class Papel(str, Enum):
    admin = "admin"
    operador = "operador"


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    papel: Papel = Papel.operador

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome": "João Silva",
                "email": "joao@empresa.com",
                "senha": "minhasenha123",
                "papel": "operador",
            }
        }
    }


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "joao@empresa.com",
                "senha": "minhasenha123",
            }
        }
    }


class Token(BaseModel):
    access_token: str
    token_type: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    papel: Papel

    model_config = {"from_attributes": True}
