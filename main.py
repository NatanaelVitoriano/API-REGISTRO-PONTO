import os
from fastapi import FastAPI
from routers import registro_ponto_routes, user_routes  # Importando o roteador
from db import Base, engine

# Configuração para o JWT
SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Incluindo as rotas dos usuários
app.include_router(user_routes.router)
app.include_router(registro_ponto_routes.router)

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)