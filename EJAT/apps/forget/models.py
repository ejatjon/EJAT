from django.db import models
from django.utils.translation import gettext_lazy as _
from register.models import MyUser


# Create your models here.
class UserMD5(models.Model):
    user_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    user_md5=models.CharField(_('user_md5'),max_length=32)
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
