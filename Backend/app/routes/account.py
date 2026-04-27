from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models import Conta, Usuario
from app.schemas import ContaCreate, ContaResponse
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/accounts", tags=["Contas"])

@router.post("/", response_model=ContaResponse, status_code=status.HTTP_201_CREATED)
def criar_conta(
    conta: ContaCreate, 
    db: Session = Depends(get_db), 
    usuario_atual: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova conta bancária ou carteira para o usuário logado.
    """
    nova_conta = Conta(
        **conta.model_dump(),
        usuario_id=usuario_atual.id 
    )
    
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)
    
    return nova_conta

@router.get("/", response_model=List[ContaResponse])
def listar_contas(
    db: Session = Depends(get_db), 
    usuario_atual: Usuario = Depends(get_current_user)
):
    """
    Lista todas as contas pertencentes ao usuário logado.
    """
    contas = db.query(Conta).filter(Conta.usuario_id == usuario_atual.id).all()
    return contas