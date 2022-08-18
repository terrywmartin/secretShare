from django.conf import settings
from django.db import models
from django import forms


from django_cryptography.fields import encrypt

from users.models import User

import uuid

# Create your models here.
class SharedSecret(models.Model):
    name = models.CharField(max_length=100, null=False, blank = False)
    text = encrypt(models.TextField(max_length=250))
    ttl = models.SmallIntegerField(default=1, null=False, blank=False)
    id = models.UUIDField(default = uuid.uuid4, unique=True,primary_key=True,editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    accessed = models.PositiveSmallIntegerField(default=0,null=False,blank=False)

    def __str__(self):
        return self.name
