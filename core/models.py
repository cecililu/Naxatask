from django.contrib.gis.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone

#Model Manger
class ProjectManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def search(self, search_string):
        return self.filter(name__icontains=search_string)
#Models

class Owner(models.Model):
    full_name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=10)
    email=models.EmailField(max_length=250) 
    def __str__(self):
        return self.full_name

class Department(models.Model):
    name=models.CharField(max_length=250)
    def __str__(self):
        return self.name
    
class Project (models.Model):
    name=models.CharField(max_length=250)
    time_started=models.DateField(auto_now=True, auto_now_add=False,blank=True,null=True)
    owner=models.ForeignKey(Owner,on_delete=models.PROTECT,null=True,blank=True)  
    site_polygon = models.MultiPolygonField(null=True, default=None,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.PROTECT, blank=True, null=True)

    is_active=models.BooleanField(default=True)
    department= models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True)

    deadline=models.DateField(blank=True, null=True)
    
    manpower = models.IntegerField(blank=True, null=True)

    #model manager
    objects= ProjectManager()

    @property
    def is_recent(self):
        # print(timezone.now.date(),"---")
        delta = timezone.now().date() - self.time_started
        print(delta,'delta')
        return delta.days <= 7

        # return self.time_started>=(timezone.now() - timezone.timedelta(days=7)).date()

    def __str__(self):
        return self.name

class OwnerProfile(models.Model):
    name=models.CharField(max_length=250)
    is_organization=models.BooleanField(default=False)
    # user=models.OneToOneField(User, null=False, primary_key=True, verbose_name='Member profile')
    # description=models.CharField(max_length=50)
    
@receiver(post_save, sender=Owner)
def OwnerProfileCreator(sender, instance, **kwargs):
    OwnerProfile(name=instance.full_name).save()

class Document(models.Model):
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to='documents/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)    
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    department=models.ForeignKey(Department,on_delete=models.PROTECT,null=True,blank=True)
    date_created=models.DateField(auto_now=False, auto_now_add=True)
    author= models.CharField(max_length=250, blank=True, null=True) 
    date_updated_on=models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name         

class ProjectSite(models.Model): 
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    project_geom=models.GeometryField(null=True,blank=True)
    user_address_point=models.GeometryField(null=True,blank=True)
    line_site_user_address=models.GeometryField(null=True,blank=True)

    def __str__(self):
        return self.project.name

# from user.models import UserProfile
class SystemSummary(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    total_projects = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    # Add other summary fields here as needed
    
    # class Meta:
    #     unique_together = ('year', 'month')
    
    def __str__(self):
        return f"{self.id}-{self.year}-{self.month} Summary"