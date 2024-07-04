from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class JWTAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123', username='testuser')
        self.token_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')

    def test_token_obtain_pair(self):
        response = self.client.post(self.token_url, {'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        # Obtain initial token pair
        response = self.client.post(self.token_url, {'email': 'test@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        # Refresh the token
        response = self.client.post(self.token_refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
