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
   path('newowner/',OwnerviewFunction,name="owner")
]