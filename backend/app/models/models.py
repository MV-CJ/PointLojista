from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
import bcrypt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'

    # Identificador único (UUID)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Campos obrigatórios para autenticação
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Método para definir a senha como hash
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Método para verificar a senha
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    # Informações básicas do usuário
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    about_me = db.Column(db.Text)
    avatar_hash = db.Column(db.String(255))  # Hash para armazenar o avatar do usuário

    # Controle de acesso e status
    account_level = db.Column(db.String(20), default='user')  # Exemplos: 'user', 'admin'
    confirmed = db.Column(db.Boolean, default=False)  # Email confirmado ou não
    blocked_attempts = db.Column(db.Integer, default=0)  # Tentativas de login incorretas
    status = db.Column(db.String(10), default='active')  # Exemplos: 'active', 'inactive'

    # Datas importantes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_access_at = db.Column(db.DateTime)

    # Telefone
    phone_number = db.Column(db.String(15), unique=True)

    # Bucket para imagens do usuário
    bucket_path = db.Column(db.String(255))  # Caminho ou identificador no bucket

    # Métodos auxiliares
    def set_password(self, password):
        """Gera o hash da senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha está correta."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}, Email: {self.email}>'
