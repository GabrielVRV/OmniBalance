from datetime import datetime, timedelta, timezone
from jose import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from app.core.config import settings

# Configura o algoritmo de hash de senha
password_hash = PasswordHash((BcryptHasher(),))

def criar_token_acesso(id_usuario: int):
    tempo_expiracao = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    dados_token = {
        "sub": str(id_usuario),
        "exp": tempo_expiracao,
        "type": "access"
    }
    
    return jwt.encode(dados_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def criar_refresh_token(id_usuario: int):
    tempo_expiracao = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    dados_token = {
        "sub": str(id_usuario),
        "exp": tempo_expiracao,
        "type": "refresh"
    }
    
    return jwt.encode(dados_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verificar_token(token: str, token_type: str = "access"):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        token_type_payload = payload.get("type")
        
        if user_id is None or token_type_payload != token_type:
            return None
            
        return int(user_id)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None