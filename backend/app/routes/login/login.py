from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, make_response, g
from werkzeug.security import check_password_hash
from app.db import db
from app.models.models import Users
from app.utils.logger_manager import logger
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from app.utils.decorators import is_authenticated, is_admin

login_bp = Blueprint("login", __name__, url_prefix="")

# Login de usuário
@login_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email or not password:
        logger.error("Email or password not provided.")
        return jsonify({"msg": "Email and password are required"}), 400

    user = Users.query.filter_by(email=email).first()
    if user is None:
        logger.error(f"User with email {email} not found.")
        return jsonify({"msg": "User not found"}), 401

    if not user.check_password(password):
        logger.error(f"Password mismatch for user {email}.")
        return jsonify({"msg": "Bad username or password"}), 401

    # Atualiza o tempo de login
    user.login_time = datetime.now(timezone.utc)
    db.session.commit()

    # Gera tokens de acesso e refresh
    access_token = create_access_token(identity=email, fresh=True)

    logger.info(f"Successful login for user {email}.")
    return jsonify({
        "access_token": access_token
    }), 200

# Logout de usuário
@login_bp.route("/logout", methods=["POST"])
@is_authenticated
def logout():
    # Agora o current_user está disponível diretamente no g
    user = g.current_user
    if user:
        user.logout_time = datetime.now(timezone.utc)
        db.session.commit()
    response = make_response(jsonify({"msg": "Logout successful"}), 200)
    unset_jwt_cookies(response)
    return response

# Rota protegida
@login_bp.route("/protected", methods=["GET"])
@is_admin
def get_protected_data():
    # Usando g.current_user diretamente
    user = g.current_user
    return jsonify({"msg": f"Welcome, {user.email}! This is protected content."}), 200
