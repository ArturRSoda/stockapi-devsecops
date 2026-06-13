from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(300))
    preco = Column(Numeric(10, 2), nullable=False)
    quantidade = Column(Integer, default=0, nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)

    fornecedor = relationship("Fornecedor")
    movimentacoes = relationship("Movimentacao", back_populates="produto")
