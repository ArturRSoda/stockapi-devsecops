from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.database import get_db
from app.models.user import Usuario
from app.schemas.user import Token, UsuarioCreate, UsuarioLogin, UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))


def criar_token(dados: dict) -> str:
    payload = dados.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    # PyJWT 1.x retorna bytes; garantir que retornamos string
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash_senha(usuario.senha),
        papel=usuario.papel.value,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.post("/login", response_model=Token)
def login(credenciais: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.email).first()
    if not usuario or not verificar_senha(credenciais.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
    token = criar_token({"sub": usuario.email, "papel": usuario.papel})
    return {"access_token": token, "token_type": "bearer"}
