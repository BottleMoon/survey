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


class UserViewSetTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('user-register')  # URL 패턴 이름이 'user-register'라고 가정합니다.
        self.valid_payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.invalid_payload = {
            'email': '',
            'username': 'testuser',
            'password': 'testpassword'
        }

    def test_register_user_with_valid_data(self):
        response = self.client.post(self.register_url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.valid_payload['email'])

    def test_register_user_with_invalid_data(self):
        response = self.client.post(self.register_url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_duplicate_email(self):
        User.objects.create_user(email='test@example.com', username='testuser1', password='testpassword')
        response = self.client.post(self.register_url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_user_with_duplicate_username(self):
        User.objects.create_user(email='test1@example.com', username='testuser', password='testpassword')
        response = self.client.post(self.register_url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)