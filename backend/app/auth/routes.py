from flask import Blueprint, request, jsonify, g, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, decode_token
from app.db import db
from app.models.models import Users
from app.components.utils.utils import is_authentic
from datetime import timedelta
import re

auth_blueprint = Blueprint('auth', __name__)

def is_valid_email(email):
    """
    Valida o formato do email usando uma expressão regular simples.
    """
    email_regex = r"(^[a-z0-9]+[.-_]?[a-z0-9]+@[a-z0-9.-]+\.[a-z]{2,}$)"
    return re.match(email_regex, email)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Verificar se todos os campos obrigatórios estão presentes
    if not email or not password or not first_name or not last_name:
        return jsonify({"message": "All fields are required!"}), 400

    # Validar email
    if not is_valid_email(email):
        return jsonify({"message": "Invalid email format!"}), 400

    # Verificar se o email já está registrado
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already exists!"}), 400

    # Cria um novo usuário com os dados fornecidos
    hashed_password = generate_password_hash(password)
    new_user = Users(
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name
    )

    # Adiciona o novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Users.query.filter_by(email=email).first()

    # Verifica se o hash da senha bate
    if user and check_password_hash(user.password, password):
        # Gerando o token JWT
        access_token = create_access_token(identity=user.email)

        return jsonify({
            "message": "Login successful!",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 401


@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    """
    Rota de logout. Quando o usuário se desloga, o token é adicionado à blacklist.
    """
    jwt_token = request.headers.get('Authorization', None)

    if jwt_token:
        token = jwt_token.split(" ")[1]  # Ignorar "Bearer"
        decoded_token = decode_token(token)
        jti = decoded_token['jti']

        # Adicionar token à blacklist por 1 dia
        current_app.redis.setex(jti, timedelta(days=1), 1)

        return jsonify({"message": "Logged out successfully!"}), 200
    else:
        return jsonify({"message": "Missing token!"}), 400


@auth_blueprint.route('/protected', methods=['GET'])
@is_authentic
def protected():
    """
    Rota protegida, acessível apenas para usuários autenticados via JWT no cabeçalho.
    """
    return jsonify({"message": f"Hello, {g.current_user.first_name}!"}), 200
