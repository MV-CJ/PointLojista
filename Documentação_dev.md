Aqui está toda a documentação consolidada em Markdown:

# Autenticação JWT com Flask

## Introdução

Este documento explica como configurar e usar autenticação baseada em JSON Web Tokens (JWT) em uma aplicação Flask. Abordaremos a configuração básica, a definição de modelos de usuários, o middleware para verificar tokens revogados, e as rotas para login e logout.

## Passo a Passo

### 1. Configuração da Aplicação Flask com JWT (`__init__.py`)

```python
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
from app.db import db
from app.routes.apiCall import blueprints
from app.utils.middleware import check_if_token_is_revoked

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
with app.app_context():
    db.create_all()
    db.engine.connect()
for blueprint, url_prefix in blueprints:
    app.register_blueprint(blueprint, url_prefix=url_prefix)
jwt.token_in_blocklist_loader(check_if_token_is_revoked)
```

> Explicação:
    Inicializa uma aplicação Flask.
    Configura CORS para permitir acessos de diferentes origens.
    Carrega configurações do Flask.
    Inicializa o JWTManager para gerenciar tokens JWT.
    Configura o banco de dados.
    Registra blueprints (rotas) e configura a função check_if_token_is_revoked para verificação de tokens revogados.

### 2. Modelo de Usuários (models.py)
```python
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    login_time = db.Column(db.DateTime, nullable=True)
    logout_time = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def has_logged_out(self):
        return self.logout_time is not None
    
    def is_token_valid(self):
        if self.logout_time is None:
            return True  
        if self.login_time is None:
            return False 
        return self.logout_time < self.login_time
```

> Explicação:
    Define a estrutura da tabela de usuários no banco de dados.
    Métodos para hash e verificação de senhas.
    Método is_token_valid() para verificar se o token do usuário é válido baseado no tempo de login e logout.

### 3. Middleware para Verificação de Token Revogado (middleware.py)

```python
from flask_jwt_extended import get_jwt_identity
from app.models.models import Users

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_data):
    decrypted_token = jwt_data  
    user_email = decrypted_token['sub']  
    user = Users.query.filter_by(email=user_email).first()
    if user is None:
        return True  
    return not user.is_token_valid()
```

> Explicação:
    Função decorada como token_in_blocklist_loader para ser chamada pelo JWTManager.
    Verifica se o usuário existe e se o token é válido com base no estado do usuário no banco de dados.

### 4. Rotas de Login e Logout (login.py)
```python
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.db import db
from app.models.models import Users
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies

login_bp = Blueprint("login", __name__, url_prefix="")

@login_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = Users.query.filter_by(email=email).first()
    if user and user.check_password(password):
        user.login_time = datetime.now(timezone.utc)
        db.session.commit()
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200
    return jsonify({"msg": "Credenciais inválidas"}), 401

@login_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(email=current_user).first()
    if user:
        user.logout_time = datetime.now(timezone.utc)
        db.session.commit()
    response = jsonify({"msg": "Logout bem-sucedido"})
    unset_jwt_cookies(response)
    return response, 200

@login_bp.route("/protected", methods=["GET"])
@jwt_required()
def get_protected_data():
    return jsonify({"msg": f"Welcome, {get_jwt_identity()}!"}), 200
```

> Explicação: Por que jwt.token_in_blocklist_loader(check_if_token_is_revoked)?
jwt.token_in_blocklist_loader(check_if_token_is_revoked)
Chamar jwt.token_in_blocklist_loader(check_if_token_is_revoked) no arquivo __init__.py é crucial por várias razões:

Configuração do JWTManager: Registra a função check_if_token_is_revoked para que o JWTManager saiba como verificar se um token foi revogado sempre que for necessário.

Verificação Automática de Tokens Revogados: Com essa configuração, a cada tentativa de acesso a rotas protegidas, o JWTManager automaticamente verifica se o token foi revogado antes de permitir o acesso.

Centralização da Lógica de Revogação: Coloca toda a lógica de verificação de tokens revogados no ponto central de configuração, evitando a necessidade de repetição em várias partes do código.

Segurança: Permite a revogação imediata de tokens comprometidos, garantindo que apenas tokens válidos e não revogados possam ser usados para acessar recursos sensíveis.

Fluxo de Autenticação: Garante que somente tokens válidos e não revogados sejam usados no fluxo de autenticação, evitando o uso de tokens antigos após logout ou alteração de senha.

Flexibilidade: Permite alterar a lógica de verificação de tokens revogados (como trocar o armazenamento) sem afetar a configuração global da aplicação.

    
    Login: Gera tokens JWT quando as credenciais são corretas.
    
    Logout: Marca o tempo de logout e invalida o token atual.
    
    Protected Route: Exemplo de rota que requer autenticação JWT.


Este setup oferece um sistema robusto de autenticação e autorização baseado em JWT para uma aplicação Flask.