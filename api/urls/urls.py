from django.urls import include, path
from rest_framework import routers
from api.viewsets.viewsets import *
router = routers.SimpleRouter()
router.register(r'projects', ProjectView)
router.register(r'owners', OwnerView)
router.register(r'projects', ProjectView)
router.register(r'departments', DepartmentView)


urlpatterns = [
   path('', include(router.urls)),
   path('documents/', DocumentListView.as_view(), name='document-list'),
   path('getshapefile/', ProjectShapefileView.as_view(), name='document-list'),
   path('newowner/',OwnerviewFunction,name="owner"),
   path('userinfo/',userinformations,name="userinformation"),
   path('files/',getfiles,name="getfile"),
   path('userstats/',getstats,name='userstat'),
   path('userstats1/',getstats1,name='userstat'),
   path('projectsummary/',projectSummary,name='projectsummary'),
   # path('projectsummary2/',projectSummary2,name='projectsummary')

]