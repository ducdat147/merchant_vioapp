from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from core.accounts.models import User


User = get_user_model()

class AccountTests(APITestCase):
    def test_create_user(self):
        url = reverse('accounts:register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'phone': '1234567890'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_login_user(self):
        User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        url = reverse('accounts:login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class PhoneNumberTest(TestCase):
    def test_valid_phone_numbers(self):
        test_cases = [
            ('0987654321', '+84987654321'),
            ('84987654321', '+84987654321'),
            ('+84987654321', '+84987654321'),
            ('0123456789', '+84123456789'),
        ]
        
        for input_phone, expected in test_cases:
            user = User.objects.create_user(
                username=f'test_user_{input_phone}',
                password='testpass123',
                phone=input_phone
            )
            self.assertEqual(str(user.phone), expected)
            
    def test_invalid_phone_numbers(self):
        invalid_numbers = [
            '12345',  # quá ngắn
            '0123456',  # không đủ số
            'abcdefghij',  # không phải số
            '01234567890',  # quá dài
            '1234567890',  # không có mã vùng
        ]
        
        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                User.objects.create_user(
                    username=f'test_user_{number}',
                    password='testpass123',
                    phone=number
                )
