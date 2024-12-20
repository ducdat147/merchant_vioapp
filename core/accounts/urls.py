from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from core.accounts.views import RegisterView, LoginView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
