from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.conf import settings
from .models import UserProfile ,User, UserSetting

def create_update_profile(sender, instance, created, **kwargs):
    if created:
        user = instance

        profile = UserProfile.objects.create(user = user, name = user.first_name + ' ' + user.last_name, email = user.email_address)
    else:
        user = instance
        profile = user.UserProfile

        profile.name = user.first_name + ' ' + user.last_name
        profile.save()

def create_user_settings(sender, instance, created, **kwargs):
    if created:
        profile = instance
        usersettings = UserSetting.objects.create(profile=profile)

def deleted_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()    

post_save.connect(create_update_profile, sender=User)
post_save.connect(create_user_settings, sender=UserProfile)
#post_delete.connect(deleted_user, sender = UserProfile)



