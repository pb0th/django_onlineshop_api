from django.test import TestCase
from products.models import Product
from categories.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from .base_product_test_case import BaseProductTestCase

from categories.models import Category

class ProductModelTest(BaseProductTestCase):
    
    def test_create_product(self):
        product = Product.objects.create(
            name=self.product_data['name'],
            description=self.product_data['description'],
            retail_price=self.product_data['retail_price'],
            cost_price=self.product_data['cost_price'],
            image=self.product_data['image'],
            is_active=self.product_data['is_active']
        )
        product.categories.set(self.product_data['categories'])
        product.save()
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, self.product_data['name'])
        self.assertEqual(product.description, self.product_data['description'])
        self.assertEqual(product.cost_price, self.product_data['cost_price'])
        self.assertEqual(product.retail_price, self.product_data['retail_price'])
        self.assertEqual(len(self.product_data['categories']), len(product.categories.all()))
    
    def test_create_product_default_is_active_true(self):
        product = Product.objects.create(
            name=self.product_data['name'],
            description=self.product_data['description'],
            retail_price=self.product_data['retail_price'],
            cost_price=self.product_data['cost_price'],
            image=self.product_data['image'],
        )
        product.categories.set(self.product_data['categories'])
        product.save()
        self.assertTrue(product.is_active)
    

    



   
    