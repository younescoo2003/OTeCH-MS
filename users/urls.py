from django.urls import path
from .views import LoginView, SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User authentication endpoints
    path('login/', LoginView.as_view(), name='user-login'),
    path('send-otp/', SendOTPView.as_view(), name='user-send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='user-verify-otp'),
    path('refresh/', TokenRefreshView.as_view(), name='user-token-refresh')
]
