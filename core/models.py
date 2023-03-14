from django.db import models

# Create your models here.
class Owner (models.Model):
    full_name=models.CharFeild(max_length=50)
    mobile_number=models.IntegerField()
    email=models.EmailField(max_length=254)
    
    def __str__(self):
        return self.name


class Project (models.Model):

    name=models.CharField(max_length=50)
    time_started=models.CharField(max_length=50)

    def __str__(self):
        return self.name
