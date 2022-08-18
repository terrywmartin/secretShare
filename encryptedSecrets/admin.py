from django.contrib import admin

from encryptedSecrets.models import SharedSecret


# Register your models here.
admin.site.register(SharedSecret)