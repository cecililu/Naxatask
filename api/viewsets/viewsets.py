from core.models import *
from rest_framework import viewsets
from api.serializers.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from zipfile import ZipFile
import os
from rest_framework import status
import json
from django.http import FileResponse
from osgeo import ogr,osr


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer=ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"message":"Success","data":serializer.data},status=status.HTTP_201_CREATED)
        except Exception  as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":str(e)})

    def update(self, request, *args, **kwargs):
        partial=kwargs.pop('partial',False)
        instance = self.get_object()
        try:
            serializer = self.serializer_class(instance, data=request.data, partial=partial)        
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(data={"message":"Success","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":str(e)})

    def delete(self,requesr,*args,**kwargs):        
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":str(e)})

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class OwnerView(viewsets.ModelViewSet):
    queryset=Owner.objects.all()
    serializer_class= OwnerSerializer


class OwnerProfileView(viewsets.ModelViewSet):
    queryset=OwnerProfile.objects.all()
    serializer_class= OwnerSerializer


class DepartmentView(viewsets.ModelViewSet):
    queryset=Department.objects.all()
    serializer_class= DepartmentSerializer
    

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        # set the user field to the current user
        serializer.save(user=self.request.user)

class DocumentListView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        department_id = request.query_params.get('department_id', None)
        date_created_min = request.query_params.get('date_created_min', None)
        date_created_max = request.query_params.get('date_created_max', None)
        queryset = Document.objects.all()
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if department_id:
            queryset = queryset.filter(project__department_id=department_id)
        if date_created_min:
            queryset = queryset.filter(date_created__gte=date_created_min)
        if date_created_max:
            queryset = queryset.filter(date_created__lte=date_created_max)
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)

#helper funnction to compute shapefile and zip it
def getShapefile(queryset):
   #extracting data from the queryset
   id=queryset.id
   wkt=queryset.site_polygon.wkt
   name_of_project=queryset.name
   owner=queryset.owner
   time_started=queryset.time_started
   geom = ogr.CreateGeometryFromWkt(wkt)

   #set up a shapefile driver and data source
   driver=ogr.GetDriverByName("ESRI Shapefile")
   ds = driver.CreateDataSource("./static/tempshapefile/projectpolygon.shp")   
   #set up projection system  
   srs=osr.SpatialReference()
   srs.ImportFromEPSG(4326)
   
   #create a layer
   layer=ds.CreateLayer("project",srs,ogr.wkbMultiPolygon) 
   
   #add a feild
   idField=ogr.FieldDefn("id",ogr.OFTInteger)
   layer.CreateField(idField)

   nameField=ogr.FieldDefn("Proj_Name",ogr.OFTString)
   layer.CreateField (nameField)

   featureDefn=layer.GetLayerDefn()
   feature=ogr.Feature(featureDefn)
   

   #Setfeild
   feature.SetGeometry(geom)
   feature.SetField("id",id)
   

   feature.SetField("Proj_Name",name_of_project)
   layer.CreateFeature(feature)
   
   feature = None
    # Save and close DataSource
   ds = None

def getZipped():
    filepath=[
        os.path.join('static/tempshapefile/projectpolygon.shp'),
        os.path.join('static/tempshapefile/projectpolygon.dbf'),
        os.path.join('static/tempshapefile/projectpolygon.prj'),
        os.path.join('static/tempshapefile/projectpolygon.shx'),
    ]

    for filename in filepath:
        print(filename)    
    
    with ZipFile('static/tempshapefile/project_shapefile.zip','w') as zip:
        for file in filepath:
            zip.write(file)

class ProjectShapefileView(APIView):
    def get(self,request):
        project_id = request.query_params.get('project_id', None)
        queryset=Project.objects.get(id=project_id)
        getShapefile(queryset)
        getZipped()
        print('ok')
        return FileResponse(
            open(os.path.join('./static/tempshapefile/project_shapefile.zip'), 'rb'),
            as_attachment=True,filename='ProjectShapefile.zip')
                


