import unittest
from app import create_app, db
from app.models.product import Product
from app import TestConfig

class ProductRoutesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_class=TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.client = self.app.test_client()
        # Add a test product to the database
        self.test_product = Product(name="prod-test", sku="test-01", quantity=100, price=10.00, category="Beverages", reorder_point=5)
        db.session.add(self.test_product)
        db.session.commit()

    def tearDown(self):
        db.session.query(Product).delete()
        db.session.commit()

    def test_get_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('prod-test', str(response.data))  
    def test_create_product(self):
        response = self.client.post('/api/products/', json={
            "name": "New Product",
            "sku": "NEW123",
            "quantity": 50,
            "price": 20.0,
            "category": "New",
            "reorder_point": 10
        })
        self.assertEqual(response.status_code, 201)  
        self.assertIn('New Product', str(response.data))  
        print(self.app.url_map)

if __name__ == '__main__':
    unittest.main()
