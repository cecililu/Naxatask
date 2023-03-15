from django.contrib.gis.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

#Model Manger
class ProjectManager(models.Manager):
    def changeName(self,name):
        self.name=name
        return self.name 

#Models
class Owner(models.Model):
    full_name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=10)
    email=models.EmailField(max_length=250) 

    def __str__(self):
        return self.full_name


class Project (models.Model):
    name=models.CharField(max_length=250)
    time_started=models.DateField(auto_now=True, auto_now_add=False,blank=True,null=True)
    owner=models.ForeignKey(Owner,on_delete=models.PROTECT,null=True,blank=True)  

    site_polygon = models.MultiPolygonField(
        null=True, blank=True, default=None
        
    )
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


#signal
@receiver(post_save, sender=Owner)
def OwnerProfileCreator(sender, instance, **kwargs):
    OwnerProfile(name=instance.full_name).save()


class Document(models.Model):
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to='documents/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    date_created=models.DateField(auto_now=False, auto_now_add=True)
    author= models.CharField(max_length=250, blank=True, null=True) 
    date_updated_on=models.DateField(auto_now=True, auto_now_add=False)
   
    def __str__(self):
        return self.name         

   