from django.urls import path
from .views import RegiterView, VerifyEmail

urlpatterns  = [
    path('register/', RegiterView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
]