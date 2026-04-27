from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models import Terceiro, Usuario
from app.schemas import TerceiroCreate, TerceiroResponse
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/third-parties", tags=["Terceiros"])

@router.post("/", response_model=TerceiroResponse, status_code=status.HTTP_201_CREATED)
def criar_terceiro(
    terceiro: TerceiroCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
):
    """
    Cria um novo terceiro para o usuário logado.
    """
    novo_terceiro = Terceiro(
        **terceiro.model_dump(),
        usuario_id=usuario_atual.id
    )
    
    db.add(novo_terceiro)
    db.commit()
    db.refresh(novo_terceiro)
    
    return novo_terceiro



@router.get("/", response_model=List[TerceiroResponse])
def listar_terceiros(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
):
    """
    Lista todos os terceiros do usuário logado.
    """
    terceiros = db.query(Terceiro).filter(Terceiro.usuario_id == usuario_atual.id).all()
    return terceiros
