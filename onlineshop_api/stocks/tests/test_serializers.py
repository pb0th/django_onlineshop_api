from .base_stock_test import BaseStockTest
from stocks.serializers import StockSerializer, StockMovementSerializer
from stocks.models import Stock


class TestStockSerializer(BaseStockTest):
    def test_serializer_create_stock_with_valid_data(self):
        serializer = StockSerializer(data=self.stock_data)
        is_valid = serializer.is_valid()
        # assert that the serializer can accept valid data
        self.assertTrue(is_valid)
        new_stock = serializer.save()
        # assert that the data is saved correctly
        self.assertEqual(new_stock.name, self.stock_data['name'])
        self.assertEqual(new_stock.quantity, self.stock_data['quantity'])
        self.assertEqual(new_stock.product.id, self.stock_data['product'])
    def test_serializer_create_stock_with_invalid_data(self):
        invalid_data = self.stock_data.copy()
        invalid_data.pop("name")
        invalid_data.pop('quantity')
        serialzier = StockSerializer(data=invalid_data)
        is_valid = serialzier.is_valid()
        self.assertFalse(is_valid)
    def test_serializer_create_stock_with_missing_product(self):
        invalid_data = self.stock_data.copy()
        invalid_data.pop("product")
        serialzier = StockSerializer(data=invalid_data)
        is_valid = serialzier.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_create_stock_with_invalid_product_id(self):
        invalid_data = self.stock_data.copy()
        invalid_data['product'] = ['asd']
        serialzier = StockSerializer(data=invalid_data)
        is_valid = serialzier.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_update_with_valid_data(self):
        update_data = {
            'name':'new name'
        }
        serializer = StockSerializer(instance=self.stock, data=update_data, partial=True)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        serializer.save()
        stock = Stock.objects.get(id=self.stock.id)
        self.assertEqual(stock.name, update_data['name'])

    def test_serializer_prevent_quantity_update(self):
        update_data = {
            'quantity':23
        }
        serializer = StockSerializer(instance=self.stock, data=update_data, partial=True)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_serializer_prevent_product_update(self):
        update_data = {
            'product':23
        }
        serializer = StockSerializer(instance=self.stock, data=update_data, partial=True)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
    

class TestStockMovementSerializer(BaseStockTest):
    def test_stock_movement_serializer_increase_stock_quantity(self):
        serializer = StockMovementSerializer(data=self.stock_movement_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        new_stock_movement = serializer.save()
        new_stock = Stock.objects.get(id=self.stock.id)
        self.assertEqual(new_stock.quantity, self.stock.quantity + self.stock_movement_data['quantity'])
        self.assertEqual(new_stock.quantity, new_stock_movement.to_quantity)
    def test_stock_movement_serializer_decrease_stock_quantity(self):
        out_data = self.stock_movement_data.copy()
        out_data['movement_type'] = "OUT"
        serializer = StockMovementSerializer(data=out_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        new_stock_movement = serializer.save()
        new_stock = Stock.objects.get(id=self.stock.id)
        self.assertEqual(new_stock.quantity, self.stock.quantity - self.stock_movement_data['quantity'])
        self.assertEqual(new_stock.quantity, new_stock_movement.to_quantity)

    def test_stock_movement_serializer_missing_stock(self):
        invalid_data = self.stock_movement_data.copy()
        invalid_data.pop("stock")
        serializer = StockMovementSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_stock_movement_serializer_missing_quantity(self):
        invalid_data = self.stock_movement_data.copy()
        invalid_data.pop("quantity")
        serializer = StockMovementSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_stock_movement_serializer_missing_movement_type(self):
        invalid_data = self.stock_movement_data.copy()
        invalid_data.pop("movement_type")
        serializer = StockMovementSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)

    def test_stock_movement_serializer_description_optional(self):
        invalid_data = self.stock_movement_data.copy()
        invalid_data.pop("description")
        serializer = StockMovementSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    

        


        

    

        

        