from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self,username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The Username must be provided]'))
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username,email, password, **extra_fields)

GENDER =(
    ('male','male'),
    ('female','female'),
)
class Profile(AbstractUser):
    username = models.CharField(max_length=20,unique=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to='profileImage',null=True)
    address_line_1 = models.CharField(max_length=255,null=True)
    address_line_2 = models.CharField(max_length=255,null=True)
    mobile_number = models.CharField(max_length=12,unique=True)
    email= models.EmailField(max_length=50,unique=True)
    gender_type = models.CharField(max_length=7,null=True,choices=GENDER)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    country = models.ForeignKey('Country', null=True, related_name='coun', on_delete=models.CASCADE)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    date_joined = models.DateTimeField(auto_now_add=True,editable=False)
    last_login = models.DateTimeField(auto_now_add=True,editable=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    password = models.CharField(max_length=1000)

    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name