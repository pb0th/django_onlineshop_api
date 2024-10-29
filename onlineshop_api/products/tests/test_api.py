from shared.base_api_test import BaseAPITest
from products.models import Product
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from categories.models import Category
from django.urls import reverse
from rest_framework import status




class ProductAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        # Create Dummy Category for testing
        self.category_1 = Category.objects.create(name="Test Name 1", description="Test Description 1")
        self.category_2 = Category.objects.create(name="Test Name 2", description="Test Description 2")
        # Create a valid in-memory image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        self.test_image_prefix = "unit_testing_image_"
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
            'quantity':23
        }
        self.product = Product.objects.create(
            name=self.product_data['name'],
            description=self.product_data['description'],
            retail_price=self.product_data['retail_price'],
            cost_price=self.product_data['cost_price'],
            image=self.product_data['image'],
            is_active=self.product_data['is_active']
        )
        self.product.categories.set(self.product_data['categories'])
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', args=[self.product.id])
    
    def test_create_product_with_valid_data(self):


        # Create a valid in-memory image for this test
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        test_image = SimpleUploadedFile(
            name=f'{self.test_image_prefix}_test_image_2.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )

        data = self.product_data.copy()
        data['image'] = test_image
        data.pop("is_active")

        
        current_product_count = Product.objects.count()
        response = self.client.post(self.list_url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(current_product_count + 1, Product.objects.count() )
        self.assertTrue(response.data['is_active'])
    
    def test_create_product_with_missing_fields(self):
        invalid_product_data = self.product_data.copy()
        invalid_product_data.pop("name")
        invalid_product_data.pop("description")
        response = self.client.post(self.list_url, data=invalid_product_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_with_missing_image_field(self):
        invalid_product_data = self.product_data.copy()
        invalid_product_data.pop("image")
        response = self.client.post(self.list_url, data=invalid_product_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_with_missing_categories_field(self):
        invalid_product_data = self.product_data.copy()
        invalid_product_data.pop("categories")
        response = self.client.post(self.list_url, data=invalid_product_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_with_empty_categories_field(self):
        invalid_product_data = self.product_data.copy()
        invalid_product_data['categories'] = []
        response = self.client.post(self.list_url, data=invalid_product_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_product_pagination(self):
        product_count = Product.objects.count()
        page = 1
        page_size = 20
        response = self.client.get(self.list_url, {'page':page, 'page_size':page_size})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product_count, response.data['count'])
        self.assertEqual(product_count, len( response.data['results']))

    def test_update_product_detail_with_valid_data(self):
   
        update_data = {
            'name':'Test Product New Name',
            'retail_price':89.00
        }
        response = self.client.patch(self.detail_url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.name, update_data['name'])
        self.assertEqual(product.retail_price, update_data['retail_price'])

    # assert that the categories remain unchanged
    def test_update_product_with_empty_categories(self):
        update_data = {
            'categories':[],
        }
        self.client.patch(self.detail_url, data=update_data)
        current_product = Product.objects.get(id=self.product.id)
        self.assertQuerySetEqual(
            current_product.categories.all(),
            self.product.categories.all(),
        )

    def test_update_other_properties_does_not_affect_is_active(self):
        update_data = {
            'is_active':False
        }
        response = self.client.patch(self.detail_url, data=update_data)
        updated_product = Product.objects.get(id=self.product.id)
        self.assertFalse(response.data['is_active'])
        self.assertFalse(updated_product.is_active)
        update_data = {
            'name':'Test New Product'
        }
        response = self.client.patch(self.detail_url, data=update_data)
        updated_product = Product.objects.get(id=self.product.id)
        self.assertFalse(response.data['is_active'])
        self.assertFalse(updated_product.is_active)

    def test_put_request_not_allowed(self):
        update_data = {
            'is_active':False
        }
        response = self.client.put(self.detail_url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_set_is_active_false(self):
        response = self.client.delete(self.detail_url)
        self.assertTrue(Product.objects.filter(id=self.product.id).exists())
        product = Product.objects.get(id=self.product.id)
        self.assertFalse(product.is_active)

        

    
        

        
    

        