from core.models import *
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = "__all__"


class DepartmentSerializer(serializer.ModelSereializer):
    class Meta:
        model = Department 
        fields = "__all__"

class OwnerSerializer(serializer.ModelSereializer):
    class Meta:
        model = Owner
        fields = "__all__"

class OwnerProfileSerializer(serializer.ModelSereializer):
    class Meta:
        model=OwnerProfile
        fields="__all__"
