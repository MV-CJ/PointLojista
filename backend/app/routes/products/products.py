from flask import Blueprint, request, jsonify, g
from app.db import db
from app.models.models import Products
from sqlalchemy.exc import IntegrityError
from app.utils.decorators import (is_authenticated, 
                                is_admin, 
                                is_manager, 
                                is_sales)

products_bp = Blueprint('products', __name__, url_prefix='/products')

# Get all products
@products_bp.route('/', methods=['GET'])
@is_sales
def get_all_products():
    products = g.tenant_filter(Products.query, Products).all()
    result = [
        {
            'id': p.id,
            'cd_ean': p.cd_ean,
            'cd_sku': p.cd_sku,
            'cd_sku_company': p.cd_sku_company,
            'name': p.name,
            'descricao': p.descricao,
            'unidade': p.unidade,
            'picture': p.picture,
            'valor_venda': p.valor_venda,
            'valor_compra': p.valor_compra,
            'margem_lucro': p.margem_lucro,
            'qty_estoque': p.qty_estoque,
            'min_estoque': p.min_estoque,
            'max_estoque': p.max_estoque,
            'fornecedor': p.fornecedor,
            'created_at': p.created_at,
            'updated_at': p.updated_at,
        }
        for p in products
    ]
    return jsonify(result), 200

# Create product
@products_bp.route('/create_product', methods=['POST'])
@is_sales
def create_product():
    try:
        data = request.get_json()
        cd_ean = data['cd_ean']
        cd_sku = data['cd_sku']
        cd_sku_company = data['cd_sku_company']
        
        # Verifica se já existe um produto com cd_ean, cd_sku ou cd_sku_company
        if Products.query.filter_by(cd_ean=cd_ean).first():
            return jsonify({'error': 'A product with this cd_ean already exists'}), 400

        if Products.query.filter_by(cd_sku=cd_sku).first():
            return jsonify({'error': 'A product with this cd_sku already exists'}), 400

        if Products.query.filter_by(cd_sku_company=cd_sku_company).first():
            return jsonify({'error': 'A product with this cd_sku_company already exists'}), 400


        new_product = Products(
            company_id=g.current_user.company_id,  # Adiciona o company_id do usuário logado
            cd_ean=data['cd_ean'],
            cd_sku=data['cd_sku'],
            cd_sku_company=data['cd_sku_company'],
            name=data['name'],
            descricao=data['descricao'],
            unidade=data['unidade'],
            picture=data.get('picture'),
            valor_venda=data['valor_venda'],
            valor_compra=data['valor_compra'],
            margem_lucro=data['margem_lucro'],
            qty_estoque=data['qty_estoque'],
            min_estoque=data['min_estoque'],
            max_estoque=data['max_estoque'],
            fornecedor=data.get('fornecedor'),
        )
        db.session.add(new_product)
        db.session.commit()
        
        # Adicionar o nome da empresa ao objeto data
        company_name = g.current_user.company.company_name if g.current_user.company else "Unknown"
        data['company_name'] = company_name  # Adiciona o nome da empresa ao data
        
        return jsonify({'message': 'Product created successfully', 'product': data}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Duplicate entry or invalid data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a single product by ID
@products_bp.route('/<int:product_id>', methods=['GET'])
@is_sales
def get_product(product_id):
    product = g.tenant_filter(Products.query, Products).filter_by(id=product_id).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    result = {
        'id': product.id,
        'cd_ean': product.cd_ean,
        'cd_sku': product.cd_sku,
        'cd_sku_company': product.cd_sku_company,
        'name': product.name,
        'descricao': product.descricao,
        'unidade': product.unidade,
        'picture': product.picture,
        'valor_venda': product.valor_venda,
        'valor_compra': product.valor_compra,
        'margem_lucro': product.margem_lucro,
        'qty_estoque': product.qty_estoque,
        'min_estoque': product.min_estoque,
        'max_estoque': product.max_estoque,
        'fornecedor': product.fornecedor,
        'created_at': product.created_at,
        'updated_at': product.updated_at,
    }
    return jsonify(result), 200

# Update a product
@products_bp.route('/<int:product_id>', methods=['PUT'])
@is_manager
def update_product(product_id):
    product = g.tenant_filter(Products.query, Products).filter_by(id=product_id).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    try:
        data = request.get_json()
        for key, value in data.items():
            setattr(product, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a product
@products_bp.route('/<int:product_id>', methods=['DELETE'])
@is_manager
def delete_product(product_id):
    product = g.tenant_filter(Products.query, Products).filter_by(id=product_id).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500