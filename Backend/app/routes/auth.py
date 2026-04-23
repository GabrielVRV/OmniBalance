from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UserCreate, UserLogin, TokenRefresh
from app.core.security import password_hash, criar_token_acesso, criar_refresh_token, verificar_token
from app.dependencies import get_db
from app.utils.password_validator import PasswordValidator

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(usuario: UserCreate, db: Session = Depends(get_db)):
    # Valida força da senha
    password_errors = PasswordValidator.validate_password(usuario.senha)
    if password_errors:
        raise HTTPException(
            status_code=400, 
            detail={"message": "Senha não atende aos requisitos de segurança", "errors": password_errors}
        )
    
    # Verifica se já existe o e-mail
    user_db = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Cria o novo usuário
    novo_user = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=password_hash.hash(usuario.senha)
    )
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return {"message": "Usuário criado com sucesso!"}

@router.post("/login")
def login(usuario: UserLogin, db: Session = Depends(get_db)):
    # Busca usuário pelo e-mail
    user_db = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    
    # Verifica se usuário existe e senha está correta
    if not user_db or not password_hash.verify(usuario.senha, user_db.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="E-mail ou senha incorretos"
        )
    
    # Verifica se usuário está ativo
    if not user_db.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuário inativo"
        )
    
    # Cria tokens de acesso e refresh
    access_token = criar_token_acesso(user_db.id)
    refresh_token = criar_refresh_token(user_db.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 30 * 60,  # 30 minutos em segundos
        "user": {
            "id": user_db.id,
            "nome": user_db.nome,
            "email": user_db.email,
            "ativo": user_db.ativo,
            "admin": user_db.admin
        }
    }

@router.post("/refresh")
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    # Verifica o refresh token
    user_id = verificar_token(token_data.refresh_token, "refresh")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Refresh token inválido ou expirado"
        )
    
    # Busca usuário no banco
    user_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    
    if not user_db or not user_db.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuário não encontrado ou inativo"
        )
    
    # Cria novo access token
    new_access_token = criar_token_acesso(user_db.id)
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 30 * 60,  # 30 minutos em segundos
    }