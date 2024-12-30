# app/routes/apiCall.py

from .products.products import products_bp
from .user import user_bp
from .login import login_bp

# Lista de blueprints para registro
blueprints = [
    (products_bp, "/api/products"),
    (user_bp, "/api/user"),
    (login_bp, "/api/"), 
]
