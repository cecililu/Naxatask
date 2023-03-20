from core.models import *
from rest_framework import viewsets
from api.serializers.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
                serializer.validated_data['created_by'] = request.user
                serializer.save()
                return Response(data={"message":"Success","data":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)
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

    def delete(self,request,*args,**kwargs):        
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_200_OK,data={"message":"Project delete successfull"})
        except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":str(e)})

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request):
        # queryset=self.get_queryset().values("id","time_started")
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=200,data={"data":serializer.data,"message":'Successful'})
        # return Response(queryset)
    

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class OwnerView(viewsets.ModelViewSet):
    queryset=Owner.objects.all()
    serializer_class= OwnerSerializer


@api_view(['GET','POST',"DELETE",'PUT',"PATCH"])
def OwnerviewFunction(request):
    pk=request.GET.get("id",False)
    #get request
    if request.method == 'GET':
        if pk==False :
            owners = Owner.objects.all()
            serializer = OwnerSerializer(owners, many=True)
            return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            owner = Owner.objects.get(pk=pk)
            serializer = OwnerSerializer(owner)
            return Response(data={"data": serializer.data, "message": "ok"}, status=status.HTTP_200_OK)
    #post request
    elif request.method=="POST":  
        serializer=OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message":"Success","data":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"message":"error could not save"})    
    #patch request
    elif request.method=="PATCH":
          owner=Owner.objects.all()
          serializer = OwnerSerializer(instance=owner, data=request.data, partial=True) 
          if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
          else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


    #delete request   
    # elif request.method == 'DELETE':
    #     if pk is not None:
    #         owner = Owner.objects.get(pk=pk)
    #         owner.delete()
    #         return Response(data={"message": "Owner deleted successfully"}, status=status.HTTP_200_OK)
    #     else:
    #         return Response(data={"message": "pk is missing"}, status=status.HTTP_400_BAD_REQUEST)


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
   ds = driver.CreateDataSource("./static/projectpolygon.shp")   
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
        # print('ok')
        return FileResponse(
            open(os.path.join('./static/tempshapefile/project_shapefile.zip'), 'rb'),
            as_attachment=True,filename='ProjectShapefile.zip')


                           
from user.models import UserProfile
from user.serializers import UserProfileSerializer,UserSerializer,UserProfileAndDataSerializer


@api_view(["GET"])
def userinformations(request):
    userid=request.GET.get("id")
    if User.objects.filter(id=userid).exists():
        user=User.objects.get(id=userid)
        userprofile=UserProfile.objects.get(user=user)

        user_serializers=UserProfileAndDataSerializer(userprofile)  
        # userprofiledata=userprofile.values("user","first_name","last_name","department","project")
       
        documents = Document.objects.filter(user=user)
        documents_serializer = DocumentSerializer(documents, many=True)

        serialized_data = user_serializers.data
        serialized_data['documents'] = documents_serializer.data 
        return Response(status=200,data={"message":"success","data":serialized_data})    
    else:
        return Response(status=400,data={"message":"user not found"})


@api_view(['GET'])
def getfiles(request):
    user_id = request.GET.get("user_id")
    depart_id = request.GET.get('depart_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    documents = Document.objects.all()

    if user_id:
        documents = documents.filter(user=user_id)
    
    if depart_id:
        documents = documents.filter(department=depart_id)

    if start_date and end_date:
        documents = documents.filter(date_created__range=[start_date, end_date])
        
    if documents.exists():
        documents_serializer = DocumentSerializer(documents, many=True)
        return Response(status=200, data={"message": "successful", "data": documents_serializer.data})
    
    return Response(status=200, data={"message": "No document found", "data": {}})




from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count

@api_view(['GET'])
def getstats(request):
    sort_by = request.query_params.get('sort_by', 'desc')
    if sort_by not in ['asc', 'desc']:
        return Response({'error': 'Invalid sort_by parameter.'}, status=400)

    project_counts = (
        Project.objects
        .annotate(month=TruncMonth('time_started'))
        .annotate(year=TruncYear('time_started'))
        .values('month', 'year', 'created_by')
        .annotate(count=Count('id'))
        .order_by('-count' if sort_by == 'desc' else 'count')
    )
    

    print('project_count',project_counts)
    data = []
    for count in project_counts:
        data.append({
            'user_id': count['created_by'],
            'month': count['month'].strftime('%B'),
            'year': count['year'].year,
            'count': count['count'],
        })

    return Response(data,status=200)

@api_view(['GET'])
def getstats1(request):
    year = request.query_params.get('year')
    month = request.query_params.get('month')
    sort_by = request.query_params.get('sort_by', 'desc')
    if sort_by not in ['asc', 'desc']:
        return Response({'error': 'Invalid sort_by parameter.'}, status=400)
     
    project_counts = (
        Project.objects
        .filter(time_started__year=year, time_started__month=month)
        .values('created_by')
        .annotate(count=Count('id'))
        .order_by('-count' if sort_by == 'desc' else 'count')
    )
    
    document_counts = (
        Document.objects
        .filter(date_created__year=year, date_created__month=month)
        .values('user')
        .annotate(count=Count('id'))
        .order_by('-count' if sort_by == 'desc' else 'count')
    )
    data=[]

    for count in project_counts:
        user_id = count['created_by']
        project_count = count['count']
        document_count = 0
        
        for doc_count in document_counts:
            if doc_count['user'] == user_id:
                document_count = doc_count['count']
                break
        
        data.append({
            'user_id': user_id,
            'project_created_count': project_count,
            'document_created_count': document_count
        })


    # data = []
    # for count in project_counts:
    #     data.append({
    #         'user_id': count['created_by'],
    #         'project_created_count': count['count'],
          
    #         # 'document_created_count':
    #     })
    # for count in document_counts:
    
    #     data.append({
    #         'user_id': count['user'],
    #         'document_created_count': count['count'],
    #         # 'document':1
    #         # 'document_created_count':
    #     })
    # data = {'project_counts': list(project_counts), 'document_counts': list(document_counts)}
    
    return Response(data={"data":data,"message":"successfull"},status=200)


# from django.db.models import Sum
from django.db.models import Count, Min,Max
# from django.db.models import Subquery, OuterRef
@api_view(['GET'])
def projectSummary(request):
    datas=Department.objects.all().values('name',).annotate(
        project_count=Count('project'),
        nearest_deadline= Min('project__deadline'),)
    for data in datas:
        if data['nearest_deadline'] is not  None:
            print( data['nearest_deadline'],"------------" )
            nearest_project = Project.objects.filter(deadline=data['nearest_deadline'])
            data['nearest_project'] = nearest_project.values("name",'id',"deadline")


    summary = {
        'total_projects': Project.objects.count(),
        'total_departments': Department.objects.count()
    }
    return Response(data={
         "data":datas,
         "summary":summary,
         "message":"successful"
                          },status=200)


from django.db.models import Count, Min
from rest_framework.response import Response
from rest_framework.decorators import api_view

# @api_view(['GET'])
# def projectSummary2(request):
#     departments = Department.objects.annotate(
#         project_count=Count('project'),
#         nearest_deadline=Min('project__deadline' )
#     ).values('name', 'project_count', 'nearest_deadline', 'project__name')
    
#     datas = []
#     for department in departments:
#         data = {
#             'department': department['name'],
#             'project_count': department['project_count'],
#             'nearest_deadline_project': {
#                 'name': department['project__name'],
#                 'nearest_deadline': department['nearest_deadline']
#             }
#         }

#     datas.append(data)
    
#     summary = {
#         'total_projects': Project.objects.count(),
#         'total_departments': Department.objects.count()
#     }

#     return Response(data={
#          "data": datas,
#          "summary": summary,
#          "message": "success"
#     }, status=200)
