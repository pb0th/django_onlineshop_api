from django.test import TestCase
from categories.models import Category
from shared.utils.delete_test_images import delete_test_images
from shared.utils.generate_test_image import generate_test_image

class BaseProductTestCase(TestCase):
    def setUp(self):
        # Create Dummy Category for testing
        self.category_1 = Category.objects.create(name="Test Name 1", description="Test Description 1")
        self.category_2 = Category.objects.create(name="Test Name 2", description="Test Description 2")
        self.test_image = generate_test_image()
        self.product_data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'retail_price': 99.99,
            'cost_price': 59.99,
            'image': self.test_image,
            'is_active': True,
            'categories': [self.category_1.id, self.category_2.id],   
        }

    def tearDown(self):
        delete_test_images('uploads/product')