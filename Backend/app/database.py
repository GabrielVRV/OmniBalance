from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Importamos as configurações do nosso config.py
from app.core.config import settings 

# Cria o motor de conexão
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ESTA É A LINHA QUE O ALEMBIC ESTÁ PROCURANDO:
Base = declarative_base()