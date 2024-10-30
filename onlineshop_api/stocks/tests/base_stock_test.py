from django.test import TestCase
from products.models import Product
from categories.models import Category
from stocks.models import Stock
from shared.utils.generate_test_image import generate_test_image
from shared.utils.delete_test_images import delete_test_images
class BaseStockTest(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(name="Test Name 1", description="Test Description 1")

        test_image = generate_test_image()
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            image=test_image,
            cost_price=99.99,
            retail_price=189.99,
            
        )
        self.product.categories.set([category_1.id])
        self.product.save()
        self.stock_data = {
            'name':'Initial Stock',
            'quantity':32,
            'product':self.product.id

        }
        self.stock = Stock.objects.create(
            name="Stock Test",
            quantity=50,
            product=self.product
        )
        self.stock_movement_data = {
            'stock': self.stock.id,
            'quantity': 50,
            'movement_type': 'IN',
            'description': 'Restocking'
        }
    def tearDown(self):
        delete_test_images('uploads/product')