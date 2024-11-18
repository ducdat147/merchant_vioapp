from rest_framework import generics, permissions
from core.merchants.models import Merchant
from core.merchants.serializers import MerchantSerializer
from drf_yasg.utils import swagger_auto_schema


class MerchantCreateView(generics.CreateAPIView):
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Create a new merchant account for authenticated user",
        responses={
            201: MerchantSerializer,
            400: "Bad Request",
            401: "Unauthorized"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MerchantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get merchant details",
        responses={
            200: MerchantSerializer,
            404: "Not Found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update merchant details",
        responses={
            200: MerchantSerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete merchant account",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class MerchantListView(generics.ListAPIView):
    serializer_class = MerchantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Merchant.objects.all()
