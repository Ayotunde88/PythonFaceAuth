from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator

class Users(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, validators=[EmailValidator()])
    phonenumber = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=255)
    purpose_of_visit = models.CharField(max_length=15, null=True, blank=True)
    visiting_whom = models.CharField(max_length=15, null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
