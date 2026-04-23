from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.core.config import settings
from app.models import Usuario

# Isso cria o cadeado no Swagger e diz onde é a rota de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 1. Gerenciador de conexão com o Banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. O "Segurança" que valida o Token e retorna o Usuário
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Putz, não consegui validar suas credenciais!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token usando as chaves do seu .env
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # Busca o dono do token no banco
    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    
    if user is None:
        raise credentials_exception
        
    return user