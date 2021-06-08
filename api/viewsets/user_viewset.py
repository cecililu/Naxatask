from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from user.models import *
from api.serializers.user_serializer import *


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.order_by('id')
    serializer_class = UserProfileSerializer
