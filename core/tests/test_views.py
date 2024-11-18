 from rest_framework import status
from django.urls import reverse
from core.tests.test_setup import TestSetUp
from core.products.models import Product
from decimal import Decimal
import os

class TestProductViews(TestSetUp):
    def test_create_product_success(self):
        """Test tạo sản phẩm mới thành công"""
        with open(self.image.name, 'rb') as image_file:
            data = {
                'name': 'Test Product',
                'description': 'Test Description',
                'price': '100.00',
                'categories': [self.category.id],
                'hashtags': [self.hashtag.id],
                'keywords': [self.keyword.id],
                'image': image_file,
                'is_active': True
            }
            
            response = self.client.post(
                reverse('products:product-list'),
                data,
                format='multipart'
            )
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Product.objects.count(), 1)
            self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_create_product_without_required_fields(self):
        """Test tạo sản phẩm thiếu thông tin bắt buộc"""
        response = self.client.post(
            reverse('products:product-list'),
            {},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('price', response.data)

    def test_get_product_list(self):
        """Test lấy danh sách sản phẩm"""
        # Tạo một số sản phẩm test
        products = [
            Product.objects.create(
                merchant=self.merchant,
                name=f'Test Product {i}',
                description='Test Description',
                price=Decimal('100.00')
            ) for i in range(3)
        ]
        
        response = self.client.get(reverse('products:product-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['count'], 3)

    def test_get_product_detail(self):
        """Test lấy chi tiết sản phẩm"""
        product = Product.objects.create(
            merchant=self.merchant,
            name='Test Product',
            description='Test Description',
            price=Decimal('100.00')
        )
        
        response = self.client.get(
            reverse('products:product-detail', kwargs={'pk': product.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')