from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    balanco = Column(Numeric(10, 2), nullable=False, default=0.00)

class Cartao(Base):
    __tablename__ = "cartoes"

    id = Column(Integer, primary_key=True, index=True)
    conta_id = Column(Integer, ForeignKey("contas.id"))
    nome = Column(String, nullable=False)
    limite = Column(Numeric(10, 2), nullable=False)
    vencimento = Column(Integer, nullable=False)
    fechamento = Column(Integer, nullable=False)
    
class Terceiro(Base):
    __tablename__ = "terceiros"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)

class Transacao(Base):
    __tablename__ = "transacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=True)
    cartao_id = Column(Integer, ForeignKey("cartoes.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    terceiro_id = Column(Integer, ForeignKey("terceiros.id"), nullable=True)
    
    valor = Column(Numeric(10, 2), nullable=False) 
    tipo = Column(String, nullable=False)
    data = Column(Date, nullable=False)
    parcela_atual = Column(Integer, nullable=False, default=1)
    parcela_total = Column(Integer, nullable=False, default=1)
    pago = Column(Boolean, default=False)
    descricao = Column(String)

class Ativo(Base):
    __tablename__ = "ativos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    ticker = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    quantidade = Column(Numeric(14, 8), nullable=False)
    preco_medio = Column(Numeric(10, 2), nullable=False)
    data_compra = Column(Date, nullable=False)