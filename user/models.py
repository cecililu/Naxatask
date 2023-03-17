# import os.path
# from io import BytesIO

from django.contrib.auth.models import User
# from django.core.files.base import ContentFile
from django.contrib.gis.db import models
# from django.utils.translation import gettext_lazy as _
# from PIL import Image

# from core.utils.managers import ActiveManager
from core.models import *
# Create your models here.
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    GENDER_CHOICES = [("Male", ("Male")), ("Female",
                                             ("Female")), ("Other", ("Other"))] 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Profile', null=True,
                             blank=True)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=15, default="Male",
                              choices=GENDER_CHOICES)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=64, blank=True, null=True)
    #added feild for pms
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ManyToManyField(Project,  null=True, blank=True)
    address_point = models.PointField(
        null=True, blank=True, default=None
    )
    way = models.LineStringField(null=True, blank=True, default=None)      
    
    def __str__(self):
        return str(self.user)

@receiver(post_save,sender=User)
def UserProfileCreator(sender, instance, created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
