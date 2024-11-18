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
        return super().post(request, *args, **kwargs)


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


class AddProductToPromotionView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        promotion_id = kwargs.get('promotion_id')
        product_id = kwargs.get('product_id')
        
        try:
            promotion = Promotion.objects.get(id=promotion_id)
            product = Product.objects.get(
                id=product_id, 
                merchant=request.user.merchant
            )
            
            promotion.products.add(product)
            return Response(
                {"message": "Product added to promotion successfully"},
                status=status.HTTP_200_OK
            )
        except (Promotion.DoesNotExist, Product.DoesNotExist):
            return Response(
                {"error": "Promotion or Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class AddServiceToPromotionView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        promotion_id = kwargs.get('promotion_id')
        service_id = kwargs.get('service_id')
        
        try:
            promotion = Promotion.objects.get(id=promotion_id)
            service = Service.objects.get(
                id=service_id, 
                merchant=request.user.merchant
            )
            
            promotion.services.add(service)
            return Response(
                {"message": "Service added to promotion successfully"},
                status=status.HTTP_200_OK
            )
        except (Promotion.DoesNotExist, Service.DoesNotExist):
            return Response(
                {"error": "Promotion or Service not found"},
                status=status.HTTP_404_NOT_FOUND
            )
