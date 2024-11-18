from django.urls import path
from core.merchants.views import (
    MerchantCreateView, 
    MerchantRetrieveUpdateDestroyView, 
    MerchantListView,
)


app_name = 'merchants'

urlpatterns = [
    path('', MerchantListView.as_view(), name='merchant-list'),
    path('create/', MerchantCreateView.as_view(), name='merchant-create'),
    path('<uuid:pk>/', MerchantRetrieveUpdateDestroyView.as_view(), name='merchant-detail'),
]
