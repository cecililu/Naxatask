from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

#Model Manger
class ProjectManager(models.Manager):
    def changeName(self,name):
        self.name=name
        return self.name 

#Models
class Owner(models.Model):
    full_name=models.CharField(max_length=100)
    mobile_number=models.IntegerField()
    email=models.EmailField(max_length=250) 

    def __str__(self):
        return self.full_name

class Project (models.Model):
    name=models.CharField(max_length=250)
    time_started=models.CharField(max_length=250)
    owner=models.ForeignKey(Owner,on_delete=models.PROTECT,null=True,blank=True)  

    objects= ProjectManager()
    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.CharField(max_length=250)
    def __str__(self):
        return self.name

class OwnerProfile(models.Model):
    name=models.CharField(max_length=250)
    is_organization=models.BooleanField(default=False)
    # description=models.CharField(max_length=50)
@receiver(post_save, sender=Owner)
def OwnerProfileCreator(sender, instance, **kwargs):
    OwnerProfile(name=instance.full_name).save()
         

