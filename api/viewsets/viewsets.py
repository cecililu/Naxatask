from core.models import *
from rest_framework import viewsets
from api.serializers.serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response


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

class ProjectShapefileView(APIView):
    def get(self,request):
        project_id = request.query_params.get('project_id', None)
        queryset=Project.objects.get(id=project_id)
        serializer=ProjectSerializer(queryset)
        # print(serializer.data)
        return Response(serializer.data)
                

