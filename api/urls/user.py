from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.viewsets import user_viewset

router = DefaultRouter()
router.register(r'user-profile', user_viewset.UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
