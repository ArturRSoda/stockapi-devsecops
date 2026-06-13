from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.supplier import Fornecedor
from app.models.user import Usuario
from app.schemas.supplier import FornecedorCreate, FornecedorResponse

router = APIRouter(prefix="/suppliers", tags=["Fornecedores"])


@router.get("", response_model=List[FornecedorResponse])
def listar_fornecedores(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return db.query(Fornecedor).all()


@router.post("", response_model=FornecedorResponse, status_code=status.HTTP_201_CREATED)
def criar_fornecedor(
    fornecedor: FornecedorCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    existente = db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor.cnpj).first()
    if existente:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    novo = Fornecedor(**fornecedor.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/{fornecedor_id}", response_model=FornecedorResponse)
def obter_fornecedor(
    fornecedor_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor


@router.put("/{fornecedor_id}", response_model=FornecedorResponse)
def atualizar_fornecedor(
    fornecedor_id: int,
    dados: FornecedorCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(fornecedor, campo, valor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor


@router.delete("/{fornecedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_fornecedor(
    fornecedor_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    db.delete(fornecedor)
    db.commit()
