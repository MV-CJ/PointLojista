from flask import jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.models import Users
from flask import current_app  # Importar current_app para acessar app.redis

def load_user_from_identity(identity):
    """
    Busca o usuário no banco de dados com base na identidade fornecida pelo JWT.
    """
    return Users.query.filter_by(email=identity).first()

def is_authentic(func):
    @jwt_required()  # Garante que o JWT seja passado no cabeçalho da requisição
    def wrapper(*args, **kwargs):
        # Obtém a identidade (email) do JWT
        current_user_email = get_jwt_identity()
        
        # Carrega o usuário a partir da identidade (email)
        user = load_user_from_identity(current_user_email)
        
        if user is None:
            return jsonify({"message": "User not found!"}), 404
        
        # Salva o usuário carregado em g, para ser acessado pela rota
        g.current_user = user
        
        # Aqui você pode pegar informações do JWT se necessário
        jwt_header = get_jwt()  # Agora a função está definida corretamente
        
        # Obter o 'jti' do token JWT
        jti = jwt_header['jti']
        
        # Verificar se o token está na blacklist usando app.redis
        if current_app.redis.get(jti):  # Usar current_app.redis
            return jsonify({"message": "Token is blacklisted!"}), 401
        
        return func(*args, **kwargs)
    return wrapper
