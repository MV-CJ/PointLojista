from datetime import timedelta
import os

class Config:
    # Chaves de segurança
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Defina uma chave secreta local para desenvolvimento
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")  # Defina uma chave JWT secreta local

    # Configuração do Banco de Dados
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")  # Usar SQLite localmente para desenvolvimento
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evitar overhead no SQLAlchemy

    # Configurações de Expiração do JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))  # 1 hora por padrão
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES')))  # 1 dia por padrão

