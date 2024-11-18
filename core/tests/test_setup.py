from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.merchants.models import Merchant
from core.products.models import Category, Hashtag, Keyword
import tempfile
from PIL import Image

User = get_user_model()

class TestSetUp(APITestCase):
    def setUp(self):
        # Tạo user test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Tạo merchant
        self.merchant = Merchant.objects.create(
            user=self.user,
            name='Test Merchant',
            description='Test Description',
            address='Test Address'
        )
        
        # Tạo category, hashtag, keyword test
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        self.hashtag = Hashtag.objects.create(
            name='testhashtag'
        )
        
        self.keyword = Keyword.objects.create(
            name='testkeyword'
        )
        
        # Tạo temporary image cho test
        self.image = self.create_test_image()
        
        # Authenticate user
        self.client.force_authenticate(user=self.user)
        
        return super().setUp()

    def tearDown(self):
        # Cleanup sau mỗi test
        if hasattr(self, 'image'):
            self.image.close()
        return super().tearDown()

    @staticmethod
    def create_test_image():
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            image = Image.new('RGB', (100, 100), 'white')
            image.save(f, 'JPEG')
            f.seek(0)
            return f