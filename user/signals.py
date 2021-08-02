from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver

from user.models import UserProfile


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, raw, **kwargs):
    if created:
        profile = UserProfile.objects.create(
            user=instance, email=instance.email, middle_name='')
    else:
        profile = UserProfile.objects.get(user=instance)
    first_name, last_name, email, middle_name = instance.first_name, instance.last_name, instance.email, ''
    if first_name and last_name:
        profile.first_name = first_name
        profile.last_name = last_name
        profile.middle_name = middle_name
        profile.email = email
        profile.save()
