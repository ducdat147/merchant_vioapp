from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.merchants.models import Merchant
from core.products.models import (
    Category, 
    Hashtag,
    Keyword, 
    Product,
    Promotion
)
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from PIL import Image
import io


User = get_user_model()

class ProductTests(APITestCase):
    def setUp(self):
        # Tạo user test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Tạo merchant
        self.merchant = Merchant.objects.create(
            user=self.user,
            name='Test Merchant',
            address='Test Address'
        )
        
        # Tạo category test
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        # Tạo hashtag test
        self.hashtag = Hashtag.objects.create(
            name='testhashtag'
        )
        
        # Tạo keyword test
        self.keyword = Keyword.objects.create(
            name='testkeyword'
        )
        
        # Đăng nhập user
        self.client.force_authenticate(user=self.user)

    def test_create_product(self):
        url = reverse('products:product-list')
        
        # Tạo một file ảnh test hợp lệ
        # Tạo ảnh test bằng PIL
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(file, 'JPEG')
        file.name = 'test.jpg'
        file.seek(0)
        
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '100.00',
            'category_ids': [str(self.category.id)],
            'hashtag_ids': [str(self.hashtag.id)],
            'keyword_ids': [str(self.keyword.id)],
            'image': file
        }
        
        response = self.client.post(url, data, format='multipart')
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_get_product_list(self):
        Product.objects.create(
            merchant=self.merchant,
            name='Test Product',
            description='Test Description',
            price=Decimal('100.00')
        )
        
        url = reverse('products:product-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class PromotionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.merchant = Merchant.objects.create(
            user=self.user,
            name='Test Merchant',
            address='Test Address'
        )
        self.client.force_authenticate(user=self.user)
        
        # Tạo product test
        self.product = Product.objects.create(
            merchant=self.merchant,
            name='Test Product',
            description='Test Description',
            price=Decimal('100.00')
        )

    def test_create_promotion(self):
        url = reverse('products:promotion-list')
        data = {
            'name': 'Test Promotion',
            'description': 'Test Description',
            'discount_percent': '10.00',
            'start_date': timezone.now().isoformat(),
            'end_date': (timezone.now() + timedelta(days=7)).isoformat(),
            'products': [str(self.product.id)]
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Promotion.objects.count(), 1)
        self.assertEqual(Promotion.objects.get().name, 'Test Promotion')

    def test_add_product_to_promotion(self):
        promotion = Promotion.objects.create(
            name='Test Promotion',
            description='Test Description',
            discount_percent=Decimal('10.00'),
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=7)
        )
        
        url = reverse('products:add-product-to-promotion', kwargs={
            'promotion_id': promotion.id,
            'product_id': self.product.id
        })
        
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.product in Promotion.objects.get(id=promotion.id).products.all()
        )
