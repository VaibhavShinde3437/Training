from django.contrib import admin
from django.urls import path,include
from .views import RegisterView, EmailverifyView, LoginView, ChangePasswordView, LogoutView, UserPorfileAPI, UpdateProfileView
from rest_framework import authentication

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:token>', EmailverifyView.as_view(), name='email-verify' ),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('login/change', ChangePasswordView.as_view(), name='update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/create/', UserPorfileAPI.as_view(), name='create-profile'),
    path('login/update', UpdateProfileView.as_view(), name='update')
]
