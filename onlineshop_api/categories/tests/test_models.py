from django.test import TestCase
from categories.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        """Set up a sample category for reusability."""
        self.category = Category.objects.create(
            name="Outer Wears",
            description="Jackets, Suits, etc",
            is_active=True
        )
    def test_create_category(self):
        """Test creating a category with valid data."""
        category = Category.objects.create(
            name="Footwear",
            description="Shoes, Sandals, etc",
            is_active=True
        )
        self.assertEqual(category.name, "Footwear")
        self.assertEqual(category.description, "Shoes, Sandals, etc")
        self.assertTrue(category.is_active)
    
    def test_str_method(self):
        """Test the __str__ method of the Category model."""
        self.assertEqual(str(self.category), "Outer Wears (Active: Yes)")
    
    def test_default_is_active_true(self):
        category = Category.objects.create(
            name="Accesories",
            description="Test Description"
        )
        self.assertTrue(category.is_active)
    
    def test_auto_now_for_updated_at(self):
        """Test that 'updated_at' is automatically updated on save."""
        old_updated_at = self.category.updated_at
        self.category.name = "New Outer Wears"
        self.category.save()
        self.assertNotEqual(self.category.updated_at, old_updated_at)

    def test_category_ordering(self):
        """Test that categories are ordered by 'created_at'."""
        cat1 = Category.objects.create(name="Category 1", description="Desc 1")
        cat2 = Category.objects.create(name="Category 2", description="Desc 2")
        categories = Category.objects.all()
        self.assertEqual(list(categories), [self.category, cat1, cat2])

    def test_verbose_name(self):
        """Test the verbose name of the Category model."""
        self.assertEqual(Category._meta.verbose_name, "Category")

    def test_verbose_name_plural(self):
        """Test the plural verbose name of the Category model."""
        self.assertEqual(Category._meta.verbose_name_plural, "Categories")

    # def test_blank_or_null_constraints(self):
    #     """Test that name and description cannot be blank or null."""
    #     with self.assertRaises(Exception):
    #         Category.objects.create(name="", description="")
        


    