from django.db.models import Q
from rest_framework import generics, permissions, status
from core.products.models import (
    Category,
    Hashtag,
    Keyword,
    Product,
    Service,
    Promotion,
)
from core.products.serializers import (
    CategorySerializer,
    HashtagSerializer,
    KeywordSerializer,
    ProductSerializer,
    ServiceSerializer,
    PromotionSerializer,
    AddServiceToPromotionSerializer,
    AddProductToPromotionSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from core.permissions import HasMerchantPermission
from django.core.exceptions import PermissionDenied


class CategoryViewSet(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class HashtagViewSet(generics.ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAuthenticated]


class KeywordViewSet(generics.ListCreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, HasMerchantPermission]
    
    def get_queryset(self):
        # Check if user is authenticated first
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        
        try:
            merchant = self.request.user.merchant
            return Product.objects.filter(merchant=merchant)
        except ObjectDoesNotExist:
            return Product.objects.none()
            
    def create(self, request, *args, **kwargs):
        try:
            if not hasattr(request.user, 'merchant'):
                return Response(
                    {"error": "You need to create a merchant before adding products"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return super().create(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                {"error": "You need to create a merchant before adding products"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    @swagger_auto_schema(
        operation_description="List all products for authenticated merchant",
        responses={
            200: ProductSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new product",
        responses={
            201: ProductSerializer,
            400: "Bad Request",
            401: "Unauthorized"
        }
    )
    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user.merchant)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            if getattr(self, 'swagger_fake_view', False):
                return Product.objects.none()
            return Product.objects.filter(merchant=self.request.user.merchant)
        except ObjectDoesNotExist:
            return Product.objects.none()


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            return Service.objects.filter(merchant=self.request.user.merchant)
        except ObjectDoesNotExist:
            return Service.objects.none()
            
    def create(self, request, *args, **kwargs):
        try:
            if not hasattr(request.user, 'merchant'):
                return Response(
                    {"error": "You need to create a merchant before adding services"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return super().create(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                {"error": "You need to create a merchant before adding services"},
                status=status.HTTP_403_FORBIDDEN
            )


class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            return Service.objects.filter(merchant=self.request.user.merchant)
        except ObjectDoesNotExist:
            return Service.objects.none()


class PromotionListCreateView(generics.ListCreateAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            merchant = self.request.user.merchant
            return Promotion.objects.filter(
                Q(products__merchant=merchant) | 
                Q(services__merchant=merchant)
            ).distinct()
        except ObjectDoesNotExist:
            return Promotion.objects.none()
            
    def create(self, request, *args, **kwargs):
        try:
            if not hasattr(request.user, 'merchant'):
                return Response(
                    {"error": "You need to create a merchant before creating promotions"},
                    status=status.HTTP_403_FORBIDDEN
                )
            return super().create(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(
                {"error": "You need to create a merchant before creating promotions"},
                status=status.HTTP_403_FORBIDDEN
            )


class PromotionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        merchant = self.request.user.merchant
        return Promotion.objects.filter(
            Q(products__merchant=merchant) | 
            Q(services__merchant=merchant)
        ).distinct()


class AddProductToPromotionView(generics.CreateAPIView):
    serializer_class = AddProductToPromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        promotion = serializer.validated_data['promotion']
        product = serializer.validated_data['product']
        promotion.products.add(product)
        
    def post(self, request, *args, **kwargs):
        mutable_data = request.data.copy()
        mutable_data['promotion_id'] = kwargs.get('promotion_id')
        mutable_data['product_id'] = kwargs.get('product_id')
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {"message": "Product added to promotion successfully"},
            status=status.HTTP_201_CREATED
        )


class AddServiceToPromotionView(generics.CreateAPIView):
    serializer_class = AddServiceToPromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        promotion = serializer.validated_data['promotion']
        service = serializer.validated_data['service']
        promotion.services.add(service)
        
    def post(self, request, *args, **kwargs):
        # Add promotion_id and service_id to request data
        mutable_data = request.data.copy()
        mutable_data['promotion_id'] = kwargs.get('promotion_id')
        mutable_data['service_id'] = kwargs.get('service_id')
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {"message": "Service added to promotion successfully"},
            status=status.HTTP_201_CREATED
        )
