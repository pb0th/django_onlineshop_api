from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class BaseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com", password="TestingPassword69", phone_number="012123123", date_of_birth="2000-01-01")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)