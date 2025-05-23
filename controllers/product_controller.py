# product_controller.py
# Lógica de controle para produtos

from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import Product, db

product_bp = Blueprint('product', __name__)

@product_bp.route('/api/products/add', methods=['POST'])
@login_required
def add_product():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        description = data.get('description', '')
        if not name or price is None:
            return jsonify({'error': 'Nome e preço são obrigatórios'}), 400
        new_product = Product(name=name, price=price, description=description)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Produto adicionado com sucesso'}), 201
    except Exception as e:
        print(f"[ERRO ADD PRODUCT] {e}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Produto não encontrado'}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Produto removido com sucesso'}), 200
    except Exception as e:
        print(f"[ERRO DELETE PRODUCT] {e}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/api/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'description': p.description
        } for p in products
    ])
