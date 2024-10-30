from django.test import TestCase
from django.db import IntegrityError
from products.models import Product
from stocks.models import Stock, StockMovement
from .base_stock_test import BaseStockTest

class StockModelTest(BaseStockTest):

    def test_create_stock(self):
        """Test creating a stock instance."""
        self.assertIsInstance(self.stock, Stock)

    def test_stock_auto_timestamps(self):
        """Test that created_at and updated_at are set automatically."""
        self.assertIsNotNone(self.stock.created_at)
        self.assertIsNotNone(self.stock.updated_at)

    def test_update_stock_quantity(self):
        """Test updating the quantity of stock."""
        self.stock.quantity = 150
        self.stock.save()
        self.assertEqual(self.stock.quantity, 150)

    def test_delete_stock_without_movements(self):
        """Test that stock can be deleted if there are no movements."""
        self.stock.delete()
        self.assertFalse(Stock.objects.filter(id=self.stock.id).exists())

    def test_delete_stock_with_movements(self):
        """Test that an IntegrityError is raised when trying to delete stock with movements."""
        StockMovement.objects.create(stock=self.stock, quantity=10, from_quantity=100, to_quantity=90, movement_type='OUT')
        
        with self.assertRaises(IntegrityError) as context:
            self.stock.delete()
        
        self.assertEqual(str(context.exception), "Cannot delete stock with existing stock movements.")
