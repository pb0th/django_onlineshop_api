from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from products.serializers import ProductSerializer
from products.models import Product
from categories.models import Category
from PIL import Image
import io
from decimal import Decimal
import os
from django.conf import settings

class ProductSerializerTest(TestCase):
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

    # clean up images after the test is done
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


    def test_serializer_with_valid_data(self):
        serializer = ProductSerializer(data=self.product_data)
        is_valid = serializer.is_valid()

        self.assertTrue(is_valid)
        self.assertEqual(serializer.validated_data['name'], self.product_data['name'])
        self.assertEqual(serializer.validated_data['description'], self.product_data['description'])
        self.assertEqual(serializer.validated_data['retail_price'], Decimal(str(self.product_data['retail_price'])))
        self.assertEqual(serializer.validated_data['cost_price'], Decimal(str(self.product_data['cost_price'])))
        self.assertEqual(serializer.validated_data['is_active'], self.product_data['is_active'])
    
    def test_serializer_create_with_valid_data(self):
        serializer = ProductSerializer(data=self.product_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        product = serializer.save()

        
        self.assertEqual(product.name, self.product_data['name'])
        self.assertEqual(product.description, self.product_data['description'])
        self.assertEqual(product.retail_price, Decimal(str(self.product_data['retail_price'])))
        self.assertEqual(product.cost_price, Decimal(str(self.product_data['cost_price'])))
        self.assertTrue(product.categories.filter(id=self.category_1.id).exists())
        self.assertTrue(product.categories.filter(id=self.category_2.id).exists())

        # Construct the expected image path
        expected_path = f"uploads/product/{self.test_image.name}"
        actual_path = os.path.relpath(product.image.path, settings.MEDIA_ROOT)

        # Validate the image path and file existence
        self.assertTrue(os.path.exists(product.image.path))
        self.assertEqual(actual_path, expected_path)
    
    def test_serializer_invalid_data(self):
        invalid_product_data = self.product_data.copy()
        invalid_product_data.pop("name")
        invalid_product_data.pop("description")
        serializer = ProductSerializer(data=invalid_product_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid) 
    
    def test_serializer_invalid_categories(self):
        invalid_product_data = self.product_data.copy()
        invalid_product_data['categories'] = []
        serializer = ProductSerializer(data=invalid_product_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

        invalid_product_data['categories'] = ['1231', '213das']
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_update_with_valid_data(self):
        product = Product.objects.create(
            name='Old Product',
            description='This is an old product.',
            retail_price=50.00,
            cost_price=30.00,
            image=self.test_image,
            is_active=True,
        )
        # Create a valid in-memory image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        new_image = SimpleUploadedFile(
            name=f"{self.test_image_prefix}update_image.png",
            content=image_io.read(),
            content_type='image/jpeg'
        )
        update_data = {
            'name':'New name',
            'description':'new description',
            'categories': [self.category_1.id],
            'image':new_image
        }
        serializer = ProductSerializer(instance=product, data=update_data, partial=True)
        is_valid = serializer.is_valid()

        # check if the data is valid
        self.assertTrue(is_valid)
        updated_product = serializer.save()
        # validate the correct data is updated 
        self.assertEqual(updated_product.name, update_data['name'])
        self.assertEqual(updated_product.description, update_data['description'])

        # validate that the image is updated correctly
        # Construct the expected image path
        expected_path = f"uploads/product/{new_image.name}"
        actual_path = os.path.relpath(product.image.path, settings.MEDIA_ROOT)
        # Validate the image path and file existence
        self.assertTrue(os.path.exists(product.image.path))
        self.assertEqual(actual_path, expected_path)
