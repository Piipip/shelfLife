from flask import Blueprint, jsonify
from app.models.sale import Sale
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp.route('/daily', methods=['GET'])
def daily_report():
    today = datetime.utcnow().date()
    sales = Sale.query.filter(
        func.date(Sale.date) == today
    ).all()
    
    total_sales = sum(sale.total_amount for sale in sales)
    total_items = sum(sale.quantity for sale in sales)
    
    sales_by_type = {}
    for sale in sales:
        if sale.transaction_type not in sales_by_type:
            sales_by_type[sale.transaction_type] = 0
        sales_by_type[sale.transaction_type] += sale.total_amount
    
    return jsonify({
        'date': today.isoformat(),
        'total_sales': total_sales,
        'total_items': total_items,
        'sales_by_type': sales_by_type
    })

@bp.route('/monthly', methods=['GET'])
def monthly_report():
    today = datetime.utcnow().date()
    start_of_month = today.replace(day=1)
    
    sales = Sale.query.filter(
        func.date(Sale.date) >= start_of_month
    ).all()
    
    daily_totals = {}
    for sale in sales:
        sale_date = sale.date.date().isoformat()
        if sale_date not in daily_totals:
            daily_totals[sale_date] = 0
        daily_totals[sale_date] += sale.total_amount
    
    return jsonify({
        'month': today.strftime('%Y-%m'),
        'total_sales': sum(daily_totals.values()),
        'daily_totals': daily_totals
    })