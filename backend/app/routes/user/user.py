from flask import Blueprint, request, jsonify, make_response, g
from app.db import db
from app.models.models import Users, Company
from werkzeug.exceptions import Forbidden
from flask_jwt_extended import (create_access_token, 
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity)

from app.utils.decorators import (is_authenticated, 
                                is_admin, 
                                is_manager, 
                                is_sales)


user_bp = Blueprint("user", __name__, url_prefix="/user")


# Registro de novo usuário
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    company_name = data.get("company_name")  # Nome da empresa

    if not all([email, password, first_name, last_name, company_name]):
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    # Verificar se o e-mail já existe
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Este e-mail já está cadastrado!"}), 409

    try:
        # Inicia a transação para garantir atomicidade
        with db.session.begin_nested():
            # Criar a empresa
            new_company = Company(company_name=company_name)
            db.session.add(new_company)
            db.session.flush()  # Garante que o ID da empresa seja gerado

            # Criar o usuário vinculado à empresa recém-criada
            new_user = Users(
                email=email,
                first_name=first_name,
                last_name=last_name,
                company_id=new_company.id  # Vincula o ID da empresa ao usuário
            )
            new_user.set_password(password)
            db.session.add(new_user)

        # Confirma toda a transação
        db.session.commit()
        return jsonify({"message": "Usuário e empresa criados com sucesso!"}), 201

    except Exception as e:
        db.session.rollback()  # Reverte tudo caso algo dê errado
        return jsonify({"error": str(e)}), 500


# Perfil do usuário logado
@user_bp.route('/profile', methods=['GET'])
@is_authenticated
def profile():
    user = g.current_user

    if not user:
        return jsonify({"error": "Usuário não encontrado!"}), 404

    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "company_name": user.company.company_name if user.company else None,
        "segment": user.company.segment if user.company else None,
        "role": user.role,
        # Formata a data para o formato dia-mês-ano hora:minuto
        "created_at": user.created_at.strftime('%d/%m/%Y %H:%M') if user.created_at else None
    }

    return jsonify(user_data), 200
