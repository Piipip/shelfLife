from app import ma
from app.models.sale import Sale

class SaleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Sale
        load_instance = True
        include_fk = True
        
    id = ma.auto_field()
    product_id = ma.auto_field()
    quantity = ma.auto_field()
    total_amount = ma.auto_field()
    transaction_type = ma.auto_field()
    date = ma.auto_field()

sale_schema = SaleSchema()
sales_schema = SaleSchema(many=True)