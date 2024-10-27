import os
import shutil
from django.conf import settings
from django.test import TestCase
from categories.models import Category
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

class BaseProductTestCase(TestCase):


    def setUp(self):
        self.test_image_prefix = "unit_testing_image_"
        # Create Dummy Category for testing
        self.category_1 = Category.objects.create(name="Test Name 1", description="Test Description 1")
        self.category_2 = Category.objects.create(name="Test Name 2", description="Test Description 2")
        # Create a valid in-memory image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        self.test_image = SimpleUploadedFile(
            name=f'{self.test_image_prefix}_test_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
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