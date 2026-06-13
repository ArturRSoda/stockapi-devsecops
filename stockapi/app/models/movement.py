from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(String(10), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    produto = relationship("Produto", back_populates="movimentacoes")
