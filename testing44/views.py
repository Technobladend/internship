from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskSerializer, TaskValidateSeralizer
from .models import Task


@api_view(['GET', 'POST'])
def task_list_api_view(request):
    if request.method == 'GET':
        task = Task.objects.all()
        data = TaskSerializer(task, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = TaskValidateSeralizer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        completed = serializer.validated_data.get('completed')
        created = serializer.validated_data.get('created')

        task = Task.objects.create(
            title=title, 
            description=description, 
            completed=completed, 
            created=created)
        task.save()
        return Response(data={'task_id': task.id}, 
                        status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_api_view(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'details': 'Task does not exist'})

    if request.method == 'GET':
        data = TaskSerializer(task).data
        return Response(data=data)
    
    elif request.method == 'PUT':
        serializer = TaskValidateSeralizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task.title = serializer.validated_data.get('title')
        task.description = serializer.validated_data.get('description')
        task.completed = serializer.validated_data.get('completed')
        task.created = serializer.validated_data.get('created')
        task.save()

        return Response(data=TaskValidateSeralizer().data, 
                        status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
            




