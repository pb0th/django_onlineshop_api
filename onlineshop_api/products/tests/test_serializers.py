from products.serializers import ProductSerializer
from products.models import Product
from decimal import Decimal
import os
from django.conf import settings
from .base_product_test_case import BaseProductTestCase
from shared.utils.generate_test_image import generate_test_image

class ProductSerializerTest(BaseProductTestCase):
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
        if not is_valid:
            print("====== serializer errors ======")
            print(serializer.errors)
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

    def test_create_product_default_is_active_true(self):
        data = self.product_data.copy()
        data.pop("is_active")
        serializer = ProductSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        product = serializer.save()
        self.assertTrue(product.is_active)
    
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


        new_image = generate_test_image()
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
        # self.assertEqual(actual_path, expected_path)

    
