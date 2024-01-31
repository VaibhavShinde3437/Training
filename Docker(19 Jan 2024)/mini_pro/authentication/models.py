from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, address, dob, gender, password=None):
        if not email:
            raise ValueError(('Users must have an email address'))
        if not username:
            raise ValueError(('Users must have an username'))
       
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, password=password, first_name=first_name, last_name=last_name, address=address,dob=dob, gender=gender)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,username,first_name, last_name, address, dob, gender,password=None):
        if not password is None:
            raise ValueError(('Enter a password'))
        user = self.create_user(email,username,first_name, last_name, address, dob,gender, password)
        user.is_superuser = True
        user.is_staff=True
        user.save()
        return user

    
class User(AbstractBaseUser, PermissionsMixin):
    GENDER = [
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE')
]
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(max_length =50, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.TextField()
    dob = models.DateField(null=True)
    gender = models.CharField(choices=GENDER)
 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def tokens(user):
        return {
            "refresh" : str(RefreshToken.for_user(user)),
            "access" : str(RefreshToken.for_user(user).access_token)
    }


class UserProfile(models.Model):
    GENDER = [
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE')
]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.TextField(null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(choices=GENDER)
    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.first_name+" "+self.last_name