from django.db import models
from django.contrib.auth.models import PermissionsMixin 
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for UserProfile."""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user profile."""
        if not email:
            raise ValueError('Users must have an email address.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        
        user.save(using=self._db)

        return user
    
    
    def create_superuser(self, email, first_name, last_name, password):
        """Create and save a new superuser with given details."""

        user = self.create_user(email, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class CustomUserProfile(AbstractBaseUser, PermissionsMixin):
    """This class is used to create a custom user model."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']


    def get_full_name(self):
        return self.first_name + " " + self.last_name


    def get_short_name(self):
        return self.first_name


    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title