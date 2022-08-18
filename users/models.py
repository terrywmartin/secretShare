from xml.etree.ElementInclude import default_loader
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.

class User(AbstractUser):
   pass
    

class PasswordToken(models.Model):
    token = models.UUIDField(null=False)
    email = models.EmailField(null=False, blank=False)
    name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    user_id = models.PositiveIntegerField(null=True)
    is_staff = models.BooleanField(null=False, default=False)
    token_life = models.PositiveIntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500,blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, unique=True,primary_key=True,editable=False)

    objects = models.Manager()

    def __str__(self):
        return str(self.name)

    
    
class UserSetting(models.Model):
    ttl = models.PositiveSmallIntegerField(default=1,null=True,blank=True)
    profile = models.OneToOneField(UserProfile,null=True,blank=False,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.profile.name)
    