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

class ProductModelTest(BaseProductTestCase):
    pass
   
    