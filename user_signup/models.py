from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
# Create your models here.

class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
