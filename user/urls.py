from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()
router.register(r'user-profile', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
