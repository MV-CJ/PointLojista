from fastapi import FastAPI
from . import models, database
from .routes import router

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=database.engine)

# Inicializa a aplicação FastAPI
app = FastAPI()

# Inclui as rotas no FastAPI
app.include_router(router)
