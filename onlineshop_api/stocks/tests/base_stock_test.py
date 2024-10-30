from django.test import TestCase
from products.models import Product
from categories.models import Category
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings
from stocks.models import Stock
class BaseStockTest(TestCase):
    def setUp(self):
        category_1 = Category.objects.create(name="Test Name 1", description="Test Description 1")
        self.test_image_prefix = "unit_testing_image_"
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        test_image = SimpleUploadedFile(
            name=f'{self.test_image_prefix}_test_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
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
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/product')
        # Check if the directory exists
        if os.path.exists(uploads_dir):
            # Iterate over all files in the directory
            for filename in os.listdir(uploads_dir):
                if filename.startswith(self.test_image_prefix):
                    # Construct the full file path
                    file_path = os.path.join(uploads_dir, filename)
                    # Delete the file
                    os.remove(file_path)

            # Optionally remove the directory if it's empty after deletion
            if not os.listdir(uploads_dir):
                os.rmdir(uploads_dir)