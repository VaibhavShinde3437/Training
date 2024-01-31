from django.shortcuts import render
from .models import User, UserProfile
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from .serializer import ResgisterSerializer, EmailVerifySerializer, LoginSerializer, ChangePasswordSerializer, UserProfileSerializer, UpdateProfileSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from mini_pro import settings
import jwt
from .utils import get_token
from rest_framework import permissions



class RegisterView(generics.GenericAPIView):
    serializer_class = ResgisterSerializer
    
    def post(self, request):
        user = self.serializer_class(data=request.data)
        user.is_valid(raise_exception=True)
        # token = RefreshToken.for_user(user)
        user.save()
        userauth = user.data
        user = User.objects.get(email = userauth['email'])
        email = userauth['email']
        token = {
            "token" : get_token(user)
        }

        send_mail(
            'Localhost: Verification',  
            'Use this Token: '+str(RefreshToken.for_user(user).access_token),     
            settings.EMAIL_HOST_USER,   
            (email,),   
            fail_silently=False   
        )
        


        return Response(userauth, status=status.HTTP_201_CREATED)
    

class EmailverifyView(generics.GenericAPIView):
    serializer_class = EmailVerifySerializer
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])   
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({"email" : "Successfully Activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError :
            return Response({'error' : 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error' : 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        

        
            
            


class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer


    def put(self, request):
        user = self.serializer_class(data=request.data)
        if user.is_valid():
            if not self.request.user.check_password(user.data.get('old_password')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.request.user.set_password(user.data.get('new_password')) 
            self.request.user.save()
            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

            return Response(response)
        
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class UserPorfileAPI(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=UserProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserProfile.objects.create()
        return Response(status=status.HTTP_201_CREATED)
    

class UpdateProfileView(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer
    lookup_field = 'email'
    queryset = User.objects.all()
    def put(self, request, *args, **kwargs):
        serializer = UpdateProfileSerializer(data=request.data)
        if serializer.is_valid():
            self.request.user.first_name = serializer.data.get('first_name')
            self.request.user.last_name = serializer.data.get('last_name')
            self.request.user.address = serializer.data.get('address')
            self.request.user.dob = serializer.data.get('dob')
            self.request.user.gender = serializer.data.get('gender')
            self.request.user.save()
            return Response({"sucess" : "Details updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    


        