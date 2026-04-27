from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, account
from app.core.config import settings

app = FastAPI(
    title="OmniBalance API",
    description="API segura para o sistema OmniBalance",
    version="1.0.0"
)

# Configuração CORS - Em produção, especifique apenas os domínios permitidos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: ["http://localhost:3000", "https://seudominio.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Aqui vamos registrar as rotas de autenticação depois
app.include_router(auth.router)
app.include_router(account.router)

@app.get("/")
def home():
    return {"status": "OmniBalance Online"}