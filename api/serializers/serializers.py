from core.models import *
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = ["name","time_started","owner"]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department 
        fields = ["name"]

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model =Owner 
        fields = ["full_name","mobile_number","email"]


class OwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnerProfile
        fields=["name","is_organization"]
