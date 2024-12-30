from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from flask import jsonify
from app.models.models import Users
from datetime import datetime, timezone

jwt = JWTManager()

# Verificar se um token JWT foi revogado ou invalidado. 
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_data):
    decrypted_token = jwt_data  # O segundo argumento contém o token decodificado
    user_email = decrypted_token['sub']  # Assumindo que 'sub' contém o email do usuário
    user = Users.query.filter_by(email=user_email).first()
    if user is None:
        return True  # Token inválido se o usuário não existe
    return not user.is_token_valid()
