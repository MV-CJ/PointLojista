from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Users

# Armazena as informações de um usuário durante a request
def get_current_user():
    if 'current_user' not in g:
        user_email = get_jwt_identity()
        g.current_user = Users.query.filter_by(email=user_email).first()
    return g.current_user

# Verifica se o usuário está autenticado e aplica o filtro de tenant
def is_authenticated(fn):
    @wraps(fn)
    @jwt_required()  # Garante que o JWT foi verificado antes
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"msg": "User not authenticated"}), 401
        # Ajusta o contexto da consulta para o tenant atual
        g.tenant_filter = lambda query, model: query.filter(model.company_id == user.company_id)
        return fn(*args, **kwargs)
    return wrapper

#### Controle de Acesso ####

def is_sales(fn):
    @wraps(fn)
    @is_authenticated
    def wrapper(*args, **kwargs):
        if g.current_user.role >= 1:  # Verifica se o usuário tem acesso de vendas
            return fn(*args, **kwargs)
        return jsonify({"msg": "Access denied. Sales access required."}), 403
    return wrapper

def is_manager(fn):
    @wraps(fn)
    @is_authenticated
    def wrapper(*args, **kwargs):
        if g.current_user.role >= 2:  # Verifica se o usuário tem acesso de gerente
            return fn(*args, **kwargs)
        return jsonify({"msg": "Access denied. Manager access required."}), 403
    return wrapper

def is_admin(fn):
    @wraps(fn)
    @is_authenticated
    def wrapper(*args, **kwargs):
        if g.current_user.role == 3:  # Verifica se o usuário tem acesso de administrador
            return fn(*args, **kwargs)
        return jsonify({"msg": "Access denied. Admin access required."}), 403
    return wrapper