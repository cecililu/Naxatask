from core.models import *
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    # site_polygon = GeometryField(required=True)
    class Meta:
        model = Project 
        fields = ["id","name","time_started","owner","site_polygon","created_by",'deadline','manpower']
        extra_kwargs={'site_polygon':{'required':True}}


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department 
        fields = ["id","name"]


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model =Owner 
        fields = ["id","full_name","mobile_number","email"]



class OwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=OwnerProfile
        fields=["id","name","is_organization"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'file', 'project', 'user', 'date_created', 'author', 'date_updated_on','department')

class ProjectSiteSerializer(serializers.Serializer):
     class Meta:
        model = ProjectSite
        fields="__all__"