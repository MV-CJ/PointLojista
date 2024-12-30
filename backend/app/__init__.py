from flask import Flask, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.db import db
from app.routes.apiCall import blueprints
from app.utils.middleware import check_if_token_is_revoked

def create_app():
    app = Flask(__name__)

    # Configurar o CORS
    CORS(app, supports_credentials=True)

    # Carregar configurações
    app.config.from_object(Config)

    # Configurar JWT Manager
    jwt = JWTManager(app)

    # Inicializar banco de dados
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            db.engine.connect()
        except Exception as e:
            raise e

    # Registrar blueprints dinamicamente
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
    
    # Configurando o JWTManager para usar essa função sempre que precisar verificar se um token foi revogado.
    jwt.token_in_blocklist_loader(check_if_token_is_revoked)
    return app
