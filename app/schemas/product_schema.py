from app import ma
from app.models.product import Product

class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True
        
    id = ma.auto_field()
    name = ma.auto_field()
    sku = ma.auto_field()
    quantity = ma.auto_field()
    price = ma.auto_field()
    category = ma.auto_field()
    reorder_point = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)