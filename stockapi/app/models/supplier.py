from sqlalchemy import Column, Integer, String

from app.database import Base


class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(18), unique=True, index=True, nullable=False)
    email = Column(String(150))
    telefone = Column(String(20))
