import os, logging
from flask import Flask, request, jsonify
from .models.models import db
from .routes.routes import routes
from flask_cors import CORS 
def create_app():
    app = Flask(__name__)
    CORS(app)
    # Pega a URL do banco de dados da variável de ambiente
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configura o nível de log
    app.logger.setLevel('INFO')
    
    # Cria um manipulador de log para o terminal (stream handler)
    handler = logging.StreamHandler()

    # Configura o formato do log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Adiciona o manipulador ao logger
    app.logger.addHandler(handler)


    # Configura o log para todas as requisições
    @app.after_request
    def log_request(response):
        app.logger.info(f"Request completed: {request.method} {request.path} - Response: {response.status}")
        return response

    # Inicialize o banco de dados
    db.init_app(app)

    # Cria as tabelas no banco de dados
    with app.app_context():
        db.create_all()

    # Registre o blueprint de rotas
    app.register_blueprint(routes)

    return app
