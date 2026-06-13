from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.movement import Movimentacao
from app.models.product import Produto
from app.models.user import Usuario
from app.schemas.movement import MovimentacaoCreate, MovimentacaoResponse

router = APIRouter(prefix="/stock", tags=["Estoque"])


@router.get("/movements", response_model=List[MovimentacaoResponse])
def listar_movimentacoes(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return db.query(Movimentacao).order_by(Movimentacao.data.desc()).all()


@router.post("/movements", response_model=MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimentacao(
    mov: MovimentacaoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    produto = db.query(Produto).filter(Produto.id == mov.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if mov.tipo.value == "saida" and produto.quantidade < mov.quantidade:
        raise HTTPException(
            status_code=400,
            detail=f"Estoque insuficiente. Disponível: {produto.quantidade}",
        )

    nova = Movimentacao(
        produto_id=mov.produto_id,
        tipo=mov.tipo.value,
        quantidade=mov.quantidade,
    )
    db.add(nova)

    if mov.tipo.value == "entrada":
        produto.quantidade += mov.quantidade
    else:
        produto.quantidade -= mov.quantidade

    db.commit()
    db.refresh(nova)
    return nova
