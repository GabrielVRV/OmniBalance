from decimal import Decimal
from pydantic import BaseModel, EmailStr
from typing import Optional


### Inicio User Schemas ###
class UserBase(BaseModel):
    nome: str
    email: EmailStr

class UserCreate(UserBase):
    senha: str

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserResponse(UserBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True
### Fim User Schemas ###



### Inicio Token Schemas ###
class TokenRefresh(BaseModel):
    refresh_token: str
### Fim Token Schemas ###



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



### Inicio Terceiro Schemas ###
class TerceiroBase(BaseModel):
    nome: str

class TerceiroCreate(TerceiroBase):
    pass

class TerceiroResponse(TerceiroBase):
    id: int
    
    class Config:
        from_attributes = True
### Fim Terceiro Schemas ###
