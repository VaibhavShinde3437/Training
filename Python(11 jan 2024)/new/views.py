from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings

class RegiterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relative_link = reverse('verify-email')
        absurl = 'http://'+str(current_site)+str(relative_link)+'?token='+str(token)
        email_body= "Hi "+user.username+", user link bellow to verigy your email \n"+absurl
        data = {'email_body': email_body, 'email_subject' : 'Verify Your Email', 'to_email' : user.email}

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)
    
class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email' : 'Successfully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError :
            return Response({'error' : 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    