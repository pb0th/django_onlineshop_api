from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from categories.models import Category
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()



# Endpoint/Integration test cases

class CategoryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com", password="TestingPassword69", phone_number="012123123", date_of_birth="2000-01-01")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.category = Category.objects.create(name='Outer Wears', description='Jackets, Suits, etc')
        self.category_data = {
            'name': 'Test Name 2',
            'description': 'Test Description 2',
            'is_active' :True
        }

    def test_create_category_with_valid_data(self):
        url = reverse("category_list")
        response = self.client.post(url, data=self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
    
    def test_create_category_with_invalid_data(self):
        invalid_data = self.category_data.copy()
        invalid_data.pop("description")
        url = reverse("category_list")
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 1)

    def test_list_categories(self):
        url = reverse("category_list")
        response = self.client.get(url)
        current_categories = Category.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(current_categories), len(response.data))

    def test_get_category_detail(self):
        url = reverse("category_detail", args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)
        self.assertEqual(response.data['description'], self.category.description)
        self.assertEqual(response.data['is_active'], self.category.is_active)
    
    def test_get_category_detail_not_found(self):
        url = reverse("category_detail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category_detail(self):
        update_data = {
            'name':'new name',
            'description':'new description'
        }
        url = reverse("category_detail", args=[self.category.id])
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])
        self.assertEqual(response.data['description'], update_data['description'])
    
    def test_update_category_detail_not_found(self): 
        update_data = {
            'name':'new name',
            'description':'new description'
        }
        url = reverse("category_detail", args=[99])
        response = self.client.patch(url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    
    
