from flask import Blueprint, request, jsonify
from app import db
from app.models.sale import Sale
from app.models.product import Product
from app.schemas.sale_schema import sale_schema, sales_schema

bp = Blueprint('sales', __name__, url_prefix='/api/sales')

@bp.route('/', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    return jsonify(sales_schema.dump(sales))

@bp.route('/', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()
        product = Product.query.get_or_404(data['product_id'])
        
        if data['transaction_type'] == 'sale' and product.quantity < data['quantity']:
            return jsonify({'error': 'Insufficient stock'}), 400
            
        new_sale = Sale(
            product_id=data['product_id'],
            quantity=data['quantity'],
            total_amount=data['quantity'] * product.price,
            transaction_type=data['transaction_type']
        )
        
        if data['transaction_type'] in ['sale', 'destroyed']:
            product.quantity -= data['quantity']
        
        db.session.add(new_sale)
        db.session.commit()
        return jsonify(sale_schema.dump(new_sale)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400