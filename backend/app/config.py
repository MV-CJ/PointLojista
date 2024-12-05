from datetime import timedelta
import os

class Config:
    # Chaves de segurança
    SECRET_KEY = os.getenv("SECRET_KEY")  # Chave secreta para JWT, ou uma default
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'your_jwt_secret_key_here')  # Substitua por uma chave segura

    # Chaves Banco
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # URL do banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Evitar overhead de rastrear modificações no banco de dados

    # Configurações do JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES')))

    # Localização dos tokens
    JWT_TOKEN_LOCATION = os.getenv('JWT_TOKEN_LOCATION').split(',')

    # Cabeçalhos JWT
    JWT_HEADER_NAME = os.getenv('JWT_HEADER_NAME')
    JWT_HEADER_TYPE = os.getenv('JWT_HEADER_TYPE')
    
    # Redis    
    REDIS_URL = os.getenv('REDIS_URL')