from unicodedata import category
from django.db import models
from django.utils import timezone
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


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super(self).get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    title = models.CharField(max_length=150)
    excerpt = models.TextField(null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique_for_date='publish_date', null=False, unique=True)
    published = models.DateField(default=timezone.now)
    author = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=options, default='draft')

    image = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')

    objects = models.Manager() # The default manager.
    postobjects = PostObjects()  # The custom manager.

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) 

    class Meta:
        ordering = ['publish'] 

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)