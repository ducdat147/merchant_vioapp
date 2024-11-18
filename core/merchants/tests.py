from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.merchants.models import Merchant


User = get_user_model()

class MerchantTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_merchant(self):
        url = reverse('merchants:merchant-create')
        data = {
            'name': 'Test Merchant',
            'description': 'Test Description',
            'address': 'Test Address'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Merchant.objects.count(), 1)
        self.assertEqual(Merchant.objects.get().name, 'Test Merchant')

    def test_get_merchant_detail(self):
        merchant = Merchant.objects.create(
            user=self.user,
            name='Test Merchant',
            address='Test Address'
        )
        
        url = reverse('merchants:merchant-detail', kwargs={'pk': merchant.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Merchant')
