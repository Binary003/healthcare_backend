from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class AuthenticationTests(APITestCase):
    def test_register_and_login(self):
        payload = {"name": "Test User", "email": "TEST@example.com", "password": "VeryStrongPass!239"}
        response = self.client.post("/api/auth/register/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        login = self.client.post("/api/auth/login/", {"email": "test@example.com", "password": payload["password"]}, format="json")
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("access", login.data)
