from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.schemas.product_schema import product_schema, products_schema

bp = Blueprint('products', __name__, url_prefix='/api/products')

@bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products))

@bp.route('/', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            sku=data['sku'],
            quantity=data['quantity'],
            price=data['price'],
            category=data['category'],
            reorder_point=data.get('reorder_point', 10)
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(product_schema.dump(new_product)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        product = Product.query.get_or_404(id)
        data = request.get_json()
        
        for key, value in data.items():
            setattr(product, key, value)
            
        db.session.commit()
        return jsonify(product_schema.dump(product))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400