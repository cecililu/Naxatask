from user.models import UserProfile
from django.contrib.gis.geos import GEOSGeometry,LineString
from core.models import *


@receiver(post_save,sender=Project)
def ProjectSiteCreator(sender,instance,**kwargs):
    userprofile=UserProfile.objects.get(user=instance.created_by) 
   
    print('===========',userprofile)   
    # print(userprofile,'=====',userprofile.address_point)
    if (instance.site_polygon!=None and userprofile.address_point!=None):
        way_user_address_site=LineString(userprofile.address_point,instance.site_polygon.centroid)
        ProjectSite(project=instance,user_address_point=userprofile.address_point,line_site_user_address=way_user_address_site).save()
    else:
        ProjectSite(project=instance,user_address_point=userprofile.address_point).save()
