from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models import Categoria, Usuario
from app.schemas import CategoriaCreate, CategoriaResponse
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/categories", tags=["Categorias"])

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova categoria para o usuário logado.
    """
    nova_categoria = Categoria(
        **categoria.model_dump(),
        usuario_id=usuario_atual.id
    )
    
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    
    return nova_categoria
    
@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
):
    """
    Lista todas as categorias pertencentes ao usuário logado.
    """
    categorias = db.query(Categoria).filter(Categoria.usuario_id == usuario_atual.id).all()
    return categorias
