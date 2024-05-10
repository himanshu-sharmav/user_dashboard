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

class BlogCategory(models.Model):
    CATEGORY_CHOICES = [
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    summary = models.TextField()
    is_draft = models.BooleanField(default=False)
    def __str__(self):
        return self.title    
    

class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, related_name='appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser, related_name='doctor_appointments', on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()    