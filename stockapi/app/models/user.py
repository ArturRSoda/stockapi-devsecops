import enum
from sqlalchemy import Column, Integer, String
from app.database import Base


class Papel(str, enum.Enum):
    admin = "admin"
    operador = "operador"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)
    papel = Column(String(20), default="operador", nullable=False)
