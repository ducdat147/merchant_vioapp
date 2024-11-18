from django.urls import path
from core.products.views import (
    CategoryViewSet, HashtagViewSet, KeywordViewSet,
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    ServiceListCreateView, ServiceRetrieveUpdateDestroyView,
    PromotionListCreateView, PromotionRetrieveUpdateDestroyView,
    AddProductToPromotionView, AddServiceToPromotionView
)


app_name = 'products'

urlpatterns = [
    path('categories/', CategoryViewSet.as_view(), name='category-list'),
    path('hashtags/', HashtagViewSet.as_view(), name='hashtag-list'),
    path('keywords/', KeywordViewSet.as_view(), name='keyword-list'),
    
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<uuid:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    
    path('services/', ServiceListCreateView.as_view(), name='service-list'),
    path('services/<uuid:pk>/', ServiceRetrieveUpdateDestroyView.as_view(), name='service-detail'),
    
    path('promotions/', PromotionListCreateView.as_view(), name='promotion-list'),
    path('promotions/<uuid:pk>/', PromotionRetrieveUpdateDestroyView.as_view(), name='promotion-detail'),
    path(
        'promotions/<uuid:promotion_id>/add-product/<uuid:product_id>/',
        AddProductToPromotionView.as_view(),
        name='add-product-to-promotion'
    ),
    path(
        'promotions/<uuid:promotion_id>/add-service/<uuid:service_id>/',
        AddServiceToPromotionView.as_view(),
        name='add-service-to-promotion'
    ),
]
