# backend/app/models/models.py
import uuid
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    profile_picture = db.Column(db.String(255))
    role = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    login_time = db.Column(db.DateTime, nullable=True)
    logout_time = db.Column(db.DateTime, nullable=True)

    # Relacionamento com a empresa
    company = db.relationship('Company', back_populates='users', lazy=True) 
    
    # Método para configurar a senha de forma segura (hash)
    def set_password(self, password):
        """Define a senha com hash seguro."""
        self.password = generate_password_hash(password)

    # Método para verificar a senha
    def check_password(self, password):
        """Verifica a senha usando o hash."""
        return check_password_hash(self.password, password)

    # Método para verificar se o usuário fez logout
    def has_logged_out(self):
        """Verifica se o usuário fez logout."""
        return self.logout_time is not None
    
    # Método para verificar se o token é valido com base no tempo de login e logout
    def is_token_valid(self):
        """Verifica se o token deve ser considerado válido com base no login e logout."""
        if self.logout_time is None:
            return True  # Se não houve logout, o token é válido
        if self.login_time is None:
            return False  # Se nunca houve login, o token é inválido
        return self.logout_time < self.login_time # compara o tempo de logout com o tempo de login.


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    cd_ean = db.Column(db.String(50), unique=True, nullable=False)
    cd_sku = db.Column(db.String(50),unique=True, nullable=False)
    cd_sku_company = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    unidade = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.String(255), nullable=True)
    
    valor_venda = db.Column(db.Float, nullable=False)
    valor_compra = db.Column(db.Float, nullable=False)
    margem_lucro = db.Column(db.Float, nullable=False)
    
    qty_estoque = db.Column(db.Integer, nullable=False)
    min_estoque = db.Column(db.Integer, nullable=False)
    max_estoque = db.Column(db.Integer, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    fornecedor = db.Column(db.String(255), nullable=True)

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    segment = db.Column(db.String(100), nullable=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=True)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relacionamento com os usuários
    users = db.relationship('Users', back_populates='company', lazy=True)