from flask import Blueprint, request, jsonify
from ..models.models import db, Users

routes = Blueprint('routes', __name__)


# Rota para obter todos os usuários
@routes.route('/list_users', methods=['GET'])
def get_users():
    try:
        users = Users.query.all()
        return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])
    except Exception as e:
        # Captura outros erros inesperados
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


# Rota para criar um novo usuário
@routes.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Obtém os dados do corpo da requisição
        data = request.get_json()

        # Verifica se o e-mail já existe no banco de dados
        existing_user = Users.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'User with this email already exists'}), 400

        # Cria o novo usuário
        new_user = Users(name=data['name'], email=data['email'])
        
        # Adiciona o novo usuário ao banco de dados e confirma a transação
        db.session.add(new_user)
        db.session.commit()

        # Retorna uma resposta de sucesso
        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        # Captura outros erros inesperados
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


# Rota para atualizar um usuário existente
@routes.route('/upload_user', methods=['PUT'])
def update_user():
    data = request.get_json()  # Obtém os dados do corpo da requisição (JSON)
    user_id = data.get('id')  # Acessa o ID enviado no corpo da requisição

    if user_id is None:
        return jsonify({'message': 'ID is required'}), 400

    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    # Itera sobre os campos no corpo da requisição e atualiza dinamicamente os atributos do usuário
    for key, value in data.items():
        # Não atualiza o campo "id", pois é usado para identificar o usuário
        if key != 'id' and hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})


# Rota para deletar um usuário
@routes.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user_id = data.get('id')

    if user_id is None:
        return jsonify({'message': 'ID is required'}), 400

    user = Users.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})
