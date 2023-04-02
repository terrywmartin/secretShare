from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.conf import settings
from .models import UserProfile ,User, UserSetting

def create_update_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        first_name = user.first_name if user.first_name != '' else 'Not Given'
        last_name = user.first_name if user.last_name != '' else 'Not Given'

        profile = UserProfile.objects.create(user = user, name = first_name + ' ' + last_name, email = user.email)
    else:
        
        user = instance
        profile = UserProfile.objects.get(user=user)

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



