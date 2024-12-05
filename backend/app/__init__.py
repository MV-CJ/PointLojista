from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.config import Config
from app.db import db
import redis
from app.models.models import Users
from app.auth import auth_blueprint

def create_app():
    app = Flask(__name__)

    # Carregar configurações
    app.config.from_object(Config)

    # Obter URL do Redis
    redis_url = app.config.get('REDIS_URL')
    if not redis_url:
        raise ValueError("A URL do Redis não está configurada. Verifique a configuração de REDIS_URL.")

    # Configurar Redis
    app.redis = redis.from_url(redis_url)

    # Inicializar o JWTManager com a app
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_data):
        """
        Função que verifica se o token JWT foi revogado (está na blacklist) no Redis.
        """
        jti = jwt_data['jti']  # Obter o 'jti' (identificador único do token)
        return app.redis.get(jti) is not None  # Verifica se o token está na blacklist

    # Inicializar o db com a app
    db.init_app(app)

    # Cria as tabelas no banco de dados, caso não existam
    with app.app_context():
        try:
            db.create_all()  # Isso cria as tabelas se não existirem
            db.engine.connect()  # Tenta uma conexão direta com o banco de dados
            print("Conexão com o banco de dados bem-sucedida!")
        except Exception as e:
            print(f"Erro na conexão com o banco de dados: {e}")
            raise e

    # Registrar o blueprint para a autenticação
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
