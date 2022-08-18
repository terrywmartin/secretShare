from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import PasswordToken, UserProfile, UserSetting, User

# Register your models here.
admin.site.register(PasswordToken)
admin.site.register(UserProfile)
admin.site.register(UserSetting)
admin.site.register(User, UserAdmin)