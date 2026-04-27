from decimal import Decimal
from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema base com campos comuns
class UserBase(BaseModel):
    nome: str
    email: EmailStr

# O que o usuário envia no momento do Cadastro
class UserCreate(UserBase):
    senha: str

# O que o usuário envia no momento do Login
class UserLogin(BaseModel):
    email: EmailStr
    senha: str

# O que a API devolve para o Frontend (Segurança: sem senha aqui!)
class UserResponse(UserBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True # Permite ler os dados do SQLAlchemy automaticamente

# Schema para refresh token
class TokenRefresh(BaseModel):
    refresh_token: str



### Inicio Conta Schemas ###
class ContaBase(BaseModel):
    nome: str
    tipo: str

class ContaCreate(ContaBase):
    balanco: Decimal

class ContaResponse(ContaBase):
    id: int
    balanco: Decimal
    
    class Config:
        from_attributes = True
### Fim Conta Schemas ###


### Inicio Categoria Schemas ###
class CategoriaBase(BaseModel):
    nome: str
    tipo: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    
    class Config:
        from_attributes = True
### Fim Categoria Schemas ###