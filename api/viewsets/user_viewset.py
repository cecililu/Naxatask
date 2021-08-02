from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers.user_serializer import *
from user.models import *


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.order_by('id')
    serializer_class = UserProfileSerializer
