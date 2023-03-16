from core.models import *
from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

class ProjectSerializer(serializers.ModelSerializer):
    # site_polygon = GeometryField(required=True)
    class Meta:
        model = Project 
        fields = ["id","name","time_started","owner","site_polygon",]

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
        fields = ('id', 'name', 'file', 'project', 'user', 'date_created', 'author', 'date_updated_on')
