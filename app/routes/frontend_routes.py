from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.product import Product
from app.models.sale import Sale
from datetime import datetime
from sqlalchemy import func

bp = Blueprint('frontend', __name__)

@bp.route('/')
def landing():
    return render_template('landing.html')

@bp.route('/dashboard')
def index():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.quantity <= Product.reorder_point).count()
    today_sales = db.session.query(func.sum(Sale.total_amount)).filter(
        func.date(Sale.date) == datetime.utcnow().date()
    ).scalar() or 0
    
    return render_template('index.html',
                         total_products=total_products,
                         low_stock=low_stock,
                         today_sales=today_sales)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/products', methods=['GET'])
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@bp.route('/products/add', methods=['POST'])
def add_product():
    try:
        new_product = Product(
            name=request.form['name'],
            sku=request.form['sku'],
            quantity=int(request.form['quantity']),
            price=float(request.form['price']),
            category=request.form['category']
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding product: {str(e)}', 'error')
    
    return redirect(url_for('frontend.products'))

@bp.route('/products/<int:id>/delete', methods=['POST'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
    
    return redirect(url_for('frontend.products'))

@bp.route('/sales', methods=['GET'])
def sales():
    products = Product.query.all()
    sales = Sale.query.order_by(Sale.date.desc()).limit(10).all()
    return render_template('sales.html', products=products, sales=sales)

@bp.route('/sales/add', methods=['POST'])
def add_sale():
    try:
        product = Product.query.get_or_404(request.form['product_id'])
        quantity = int(request.form['quantity'])
        
        if request.form['transaction_type'] == 'sale' and product.quantity < quantity:
            flash('Insufficient stock', 'error')
            return redirect(url_for('frontend.sales'))
        
        new_sale = Sale(
            product_id=product.id,
            quantity=quantity,
            total_amount=quantity * product.price,
            transaction_type=request.form['transaction_type']
        )
        
        if request.form['transaction_type'] in ['sale', 'destroyed']:
            product.quantity -= quantity
        
        db.session.add(new_sale)
        db.session.commit()
        flash('Transaction recorded successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error recording transaction: {str(e)}', 'error')
    
    return redirect(url_for('frontend.sales'))

@bp.route('/reports')
def reports():
    today = datetime.utcnow().date()
    
    daily_sales = Sale.query.filter(
        func.date(Sale.date) == today
    ).all()
    
    daily_report = {
        'total_sales': sum(sale.total_amount for sale in daily_sales),
        'total_items': sum(sale.quantity for sale in daily_sales),
        'sales_by_type': {}
    }
    
    for sale in daily_sales:
        if sale.transaction_type not in daily_report['sales_by_type']:
            daily_report['sales_by_type'][sale.transaction_type] = 0
        daily_report['sales_by_type'][sale.transaction_type] += sale.total_amount
    
    start_of_month = today.replace(day=1)
    monthly_sales = Sale.query.filter(
        func.date(Sale.date) >= start_of_month
    ).all()
    
    daily_totals = {}
    for sale in monthly_sales:
        sale_date = sale.date.date().isoformat()
        if sale_date not in daily_totals:
            daily_totals[sale_date] = 0
        daily_totals[sale_date] += sale.total_amount
    
    monthly_report = {
        'total_sales': sum(daily_totals.values()),
        'daily_totals': dict(sorted(daily_totals.items()))
    }
    
    return render_template('reports.html',
                         today=today.strftime('%Y-%m-%d'),
                         month=today.strftime('%B %Y'),
                         daily_report=daily_report,
                         monthly_report=monthly_report)