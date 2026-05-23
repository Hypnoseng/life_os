from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Task

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TaskSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.filters import SearchFilter

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


@login_required
def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")

        if title:
            Task.objects.create(title=title, user=request.user)

        return redirect("task_list")

    tasks = Task.objects.filter(user=request.user)
    return render(request, "core/task_list.html", {"tasks": tasks})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()

    return redirect("task_list")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        new_title = request.POST.get("title")
        task.title = new_title
        task.save()
        return redirect("task_list")

    return render(request, "core/edit_task.html", {"task": task})


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    task.is_done = not task.is_done
    task.save()

    return redirect("task_list")

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list_api(request):

    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user).order_by("id")
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail_api(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)

ordering_fields = ['id', 'title']

class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
