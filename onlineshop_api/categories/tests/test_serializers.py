from django.test import TestCase
from categories.serializers import CategorySerializer
from categories.models import Category
class CategorySerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'name':'Test Name',
            'description':'Test Description',
            'is_active':True
        }
        self.invalid_data_empty_name = {
            'name':'',
            'description':'Test Description',
            'is_active':True
        }
        self.invalid_data_empty_description = {
            'name':'Test Name',
            'description':'',
            'is_active':True
        }
        self.invalid_data_missing_name = {
            'description':'Test Description',
            'is_active':True
        }
        self.invalid_data_missing_description = {
            'name':'Test Name',
            'is_active':True
        }
        self.invalid_data_both_empty = {
            'name': '',
            'description': '',
            'is_active': True
        }
    
    def test_serializer_valid_data(self):
        serializer = CategorySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], self.valid_data['name'])
        self.assertEqual(serializer.validated_data['description'], self.valid_data['description'])
        self.assertEqual(serializer.validated_data['is_active'], self.valid_data['is_active'])
    
    def test_serializer_invalid_data_empty_name(self):
        serializer = CategorySerializer(data=self.invalid_data_empty_name)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
    
    def test_serializer_invalid_data_empty_descriptin(self):
        serializer = CategorySerializer(data=self.invalid_data_empty_description)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_serializer_invalid_data_missing_name(self):
        serializer = CategorySerializer(data=self.invalid_data_missing_name)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_serializer_invalid_data_missing_description(self):
        serializer = CategorySerializer(data=self.invalid_data_missing_description)
        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)
    
    def test_serializer_invalid_data_both_empty(self):
        serializer = CategorySerializer(data=self.invalid_data_both_empty)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("description", serializer.errors)
    
    def test_serializer_creation(self):
        serializer = CategorySerializer(data=self.valid_data)
        if serializer.is_valid():
            category = serializer.save()
            self.assertIsInstance(category, Category)
            self.assertEqual(category.name, self.valid_data['name'])
            self.assertEqual(category.description, self.valid_data['description'])
            self.assertEqual(category.is_active, self.valid_data['is_active'])
    
    
    