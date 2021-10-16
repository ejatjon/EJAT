from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class Contact(models.Model):
    full_name = models.CharField(max_length=220, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.TextField(null=False, blank=False)
    message = HTMLField()


class TinifyException(models.Model):
    path=models.FilePathField()
    create_time=models.DateTimeField(auto_now_add=True)
    Exception=models.TextField()

class TinifyResult(models.Model):
    path = models.FilePathField()
    create_time = models.DateTimeField(auto_now_add=True)
    masage=models.CharField(max_length=128)