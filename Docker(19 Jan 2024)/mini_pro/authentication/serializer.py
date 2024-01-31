from .models import User, UserProfile
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class ResgisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, write_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '') 

        if not username:
            return serializers.ValidationError("Enter a valid username")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['token'] 

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=2,write_only=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6,read_only=True)

    class Meta:
            model = User
            fields = ['email', 'username', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Bad Credentials")
        if not user.is_verified:
            raise AuthenticationFailed("Verify your Email")
        if not user.is_active:
            raise AuthenticationFailed("Register first")
        return {
            'email':user.email,
            'username' : user.username,
            'tokens' : user.tokens()
        }
        

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'dob', 'gender']

class UpdateProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    address = serializers.CharField()
    dob = serializers.DateField()
    gender = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'dob', 'gender']


    



    


