from shared.base_api_test import BaseAPITest
from categories.models import Category
from products.models import Product
from stocks.models import Stock, StockMovement
from shared.utils.generate_test_image import generate_test_image
from django.urls import reverse
from rest_framework import status

class TestStockAPI(BaseAPITest):
    def setUp(self):
        super().setUp()
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
        self.stock_data = {
            'name':'Initial Stock',
            'quantity':32,
            'product':self.product.id
        }

        self.stock_1 = Stock.objects.create(name="Initial Stock", quantity=32, product=self.product)
        self.stock_2 = Stock.objects.create(name="Additional Stock", quantity=50, product=self.product)

        self.list_url = reverse("stock-list")
        self.detail_url = reverse('stock-detail', args=[self.stock_1.id])

    
    def test_api_create_stock_with_valid_data(self):
        current_stock_count = Stock.objects.filter(product_id=self.product.id).count()
        response = self.client.post(self.list_url, data=self.stock_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_stock_count = Stock.objects.filter(product_id=self.product.id).count()
        self.assertEqual(new_stock_count, current_stock_count + 1)

    def test_api_create_stock_with_missing_name(self):
        """Test creating stock without a name field."""
        data = self.stock_data.copy()
        data.pop('name')
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_api_create_stock_with_missing_quantity(self):
        """Test creating stock without a quantity field."""
        data = self.stock_data.copy()
        data.pop('quantity')
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)

    def test_api_create_stock_with_missing_product(self):
        """Test creating stock without a product field."""
        data = self.stock_data.copy()
        data.pop('product')
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product', response.data)

    def test_api_create_stock_with_empty_data(self):
        """Test creating stock with empty data."""
        response = self.client.post(self.list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('quantity', response.data)
        self.assertIn('product', response.data)

    def test_api_get_stock_list(self):
        """Test retrieving all stock records with pagination."""
        total_stocks = Stock.objects.count()
        page_size = 20
        total_pages = (total_stocks + page_size - 1) // page_size  # Ceiling division

        response = self.client.get(self.list_url, {'page': 1, 'page_size': page_size})
        
        # Status code check
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Dynamic pagination assertions
        self.assertEqual(response.data['count'], total_stocks)
        self.assertEqual(response.data['total_pages'], total_pages)
        self.assertEqual(response.data['current_page'], 1)
        
        # Results should be the minimum of the page size or the remaining stocks
        expected_results_count = min(page_size, total_stocks)
        self.assertEqual(len(response.data['results']), expected_results_count)

    def test_api_filter_stock_by_product(self):
        """Test filtering stock by product ID with pagination."""
        response = self.client.get(self.list_url, {'product': self.product.id, 'page': 1, 'page_size': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

    def test_api_get_stock_list_with_valid_product_filter(self):
        """Test retrieving stock records filtered by a valid product ID."""
        # Create additional stock for a different product
        product_2 = Product.objects.create(
            name='Another Product', description='Another product description',
            retail_price=150, cost_price=100, is_active=True
        )
        Stock.objects.create(name="Stock for Product 2", quantity=5, product=product_2)

        # Retrieve stocks filtered by the initial product
        expected_stocks = Stock.objects.filter(product=self.product)
        response = self.client.get(self.list_url, {'product': self.product.id, 'page': 1, 'page_size': 10})

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected_stocks.count())
        self.assertEqual(response.data['current_page'], 1)

        # Assert correct results from the filter
        returned_stock_ids = {stock['id'] for stock in response.data['results']}
        expected_stock_ids = {stock.id for stock in expected_stocks}
        self.assertSetEqual(returned_stock_ids, expected_stock_ids)

    def test_api_get_stock_list_with_quantity_filter(self):
        """Test retrieving stock records filtered by a specific quantity."""
        # Create stocks with different quantities
        Stock.objects.create(name="Stock 10", quantity=10, product=self.product)
        Stock.objects.create(name="Stock 20", quantity=20, product=self.product)

        # Filter for stocks with quantity = 10
        expected_stocks = Stock.objects.filter(quantity=10)
        response = self.client.get(self.list_url, {'quantity': 10, 'page': 1, 'page_size': 10})

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected_stocks.count())

        # Assert correct results from the filter
        returned_stock_ids = {stock['id'] for stock in response.data['results']}
        expected_stock_ids = {stock.id for stock in expected_stocks}
        self.assertSetEqual(returned_stock_ids, expected_stock_ids)

    def test_api_get_stock_list_with_multiple_filters(self):
        """Test retrieving stock records with multiple filters applied."""
        # Create an additional stock that matches the filter criteria
        Stock.objects.create(name="Matching Stock", quantity=23, product=self.product)

        # Filter for stocks with both product ID and quantity = 23
        expected_stocks = Stock.objects.filter(product=self.product, quantity=23)
        response = self.client.get(self.list_url, {
            'product': self.product.id, 
            'quantity': 23,
            'page': 1, 
            'page_size': 10
        })

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected_stocks.count())

        # Assert correct results from the filter
        returned_stock_ids = {stock['id'] for stock in response.data['results']}
        expected_stock_ids = {stock.id for stock in expected_stocks}
        self.assertSetEqual(returned_stock_ids, expected_stock_ids)

    def test_api_get_stock_list_with_name_filter(self):
        """Test retrieving stock records filtered by name."""
        Stock.objects.create(name="Special Stock", quantity=15, product=self.product)

        # Apply name filter
        expected_stocks = Stock.objects.filter(name__icontains="Special")
        response = self.client.get(self.list_url, {'name': 'Special', 'page': 1, 'page_size': 10})

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected_stocks.count())

        # Assert correct results from the filter
        returned_stock_names = {stock['name'] for stock in response.data['results']}
        expected_stock_names = {stock.name for stock in expected_stocks}
        self.assertSetEqual(returned_stock_names, expected_stock_names)


    def test_api_update_stock_name_successfully(self):
        """Test that the stock name can be updated successfully."""
        update_data = {'name': 'Updated Stock Name'}
        response = self.client.patch(self.detail_url, data=update_data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_stock = Stock.objects.get(id=self.stock_1.id)
        self.assertEqual(updated_stock.name, update_data['name'])  # Check the name update
        self.assertEqual(updated_stock.quantity, self.stock_1.quantity)  # Ensure quantity is unchanged


    def test_api_update_quantity_not_allowed(self):
        """Test that updating the quantity is not allowed."""
        update_data = {'quantity': 50}
        response = self.client.patch(self.detail_url, data=update_data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('quantity', response.data)  # Check if 'quantity' field has error

        unchanged_stock = Stock.objects.get(id=self.stock_1.id)
        self.assertEqual(unchanged_stock.quantity, self.stock_1.quantity)  # Quantity should remain unchanged


    def test_api_update_product_not_allowed(self):
        """Test that updating the product field is not allowed."""
        new_product = Product.objects.create(
            name='New Product', description='New description', retail_price=120, cost_price=80
        )
        update_data = {'product': new_product.id}
        response = self.client.patch(self.detail_url, data=update_data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product', response.data)  # Check if 'product' field has error

        unchanged_stock = Stock.objects.get(id=self.stock_1.id)
        self.assertEqual(unchanged_stock.product.id, self.product.id)  # Product should remain unchanged


    def test_api_partial_update_other_fields(self):
        """Test partial updates to fields other than quantity and product."""
        update_data = {'name': 'Partially Updated Stock'}
        response = self.client.patch(self.detail_url, data=update_data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_stock = Stock.objects.get(id=self.stock_1.id)
        self.assertEqual(updated_stock.name, update_data['name'])  # Verify name change
        self.assertEqual(updated_stock.quantity, self.stock_1.quantity)  # Quantity should remain unchanged
        self.assertEqual(updated_stock.product.id, self.product.id)  # Product should remain unchanged


    def test_api_invalid_patch_with_nonexistent_product(self):
        """Test that updating stock with a nonexistent product fails."""
        update_data = {'product': 99999}  # Non-existent product ID
        response = self.client.patch(self.detail_url, data=update_data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product', response.data)  # Ensure product field returns an error

    def test_api_delete_stock_without_movements(self):
        """Test deleting stock that has no movements."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Stock.objects.filter(id=self.stock_1.id).exists())

    def test_api_delete_stock_with_movements(self):
        """Test that deleting stock with movements raises an error."""
        StockMovement.objects.create(stock=self.stock_1, quantity=10, from_quantity=100, to_quantity=90, movement_type='OUT')
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Cannot delete stock with existing stock movements.")
        self.assertTrue(Stock.objects.filter(id=self.stock_1.id).exists())

    def test_api_delete_non_existent_stock(self):
        """Test that trying to delete a non-existent stock returns a 404 error."""
        non_existent_url = reverse('stock-detail', args=[999])  # ID that doesn't exist
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_delete_stock_returns_correct_response(self):
        """Test that the response from deleting stock is as expected."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



    

    


