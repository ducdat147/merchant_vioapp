from django.db.models import Q
from rest_framework import generics, permissions
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
from rest_framework import status


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
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Xử lý cho swagger docs
            return Product.objects.none()
        return Product.objects.filter(merchant=self.request.user.merchant)
    
    @swagger_auto_schema(
        operation_description="List all products for authenticated merchant",
        responses={
            200: ProductSerializer(many=True),
            401: "Unauthorized"
        },
        manual_parameters=[
            openapi.Parameter(
                'page', 
                openapi.IN_QUERY, 
                description="Page number", 
                type=openapi.TYPE_INTEGER
            )
        ]
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
        if getattr(self, 'swagger_fake_view', False):  # Xử lý cho swagger docs
            return Product.objects.none()
        return Product.objects.filter(merchant=self.request.user.merchant)


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Service.objects.filter(merchant=self.request.user.merchant)


class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Service.objects.filter(merchant=self.request.user.merchant)


class PromotionListCreateView(generics.ListCreateAPIView):
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        merchant = self.request.user.merchant
        return Promotion.objects.filter(
            Q(products__merchant=merchant) | 
            Q(services__merchant=merchant)
        ).distinct()


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
        # Thêm promotion_id và service_id vào request data
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
