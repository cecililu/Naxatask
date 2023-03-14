from core.models import *
from rest_framework import viewsets
from api.serializers.serializers import *

class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class OwnerView(viewsets.ModelViewSet):
    queryset=Owner.objects.all()
    serializer_class= OwnerSerializer

class OwnerProfileView(viewsets.ModelViewSet):
    queryset=OwnerProfile.objects.all()
    serializer_class= OwnerSerializer

class DepartmentView(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    serializer_class= DepartmentSerializer