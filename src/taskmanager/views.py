from taskmanager.models import Project, Task, User
from rest_framework import viewsets
from taskmanager.serializers import (
    TaskUpdateSerializer,
    UserSignupSerializer,
    ProjectSerializer,
    TaskSerializer,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from taskmanager.utils import JSONResponse
from rest_framework.generics import CreateAPIView

class CreateUserView(CreateAPIView):

    model = User
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = UserSignupSerializer


class TaskView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def is_user_manager_or_developer(user, project):
        return user == project.manager or user in project.developers.all()

    @staticmethod
    def is_user_task_assignee(user, task):
        return user in task.assignee.all()

    def list(self, request, project_id, assignee_id=None):
        """
        The method handle below tasks:
            - get projects tasks if there is only project_id in the method arguments.
            - get projects assignee tasks if there is assigne_id in the method arguments.
        """
        project = get_object_or_404(Project, pk=project_id)
        
        # Checking user is not project owner or member
        if not self.is_user_manager_or_developer(request.user, project):
            return Response(
                JSONResponse.PERMISSION_DENIED,
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if assignee_id:
            assignee = get_object_or_404(User, pk=assignee_id, projects=project)
            queryset = project.tasks.filter(assignee=assignee)
        else:
            queryset = project.tasks.all()

        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_id):
        serializer = TaskSerializer(data=request.data)
        serializer.initial_data["project"] = project_id
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, pk=project_id)

        if not self.is_user_manager_or_developer(request.user, project):
            return Response(
                JSONResponse.PERMISSION_DENIED,
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # If the assignee is not one of the project developers.
        assignee = serializer.validated_data.get("assignee")
        if assignee and not set(assignee).issubset(project.developers.all()):
            return Response(
                JSONResponse.ASSIGNE_IS_NOT_PROJ_MEMBER, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, project_id, pk=None):
        task = get_object_or_404(Task, pk=pk)
        project = get_object_or_404(Project, pk=project_id)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        assignee = serializer.validated_data.get("assignee")
        if assignee and not set(assignee).issubset(project.developers.all()):
            return Response(
                JSONResponse.ASSIGNE_IS_NOT_PROJ_MEMBER, status=status.HTTP_400_BAD_REQUEST
            )

        if not self.is_user_manager_or_developer(
            request.user, project
        ) and not self.is_user_task_assignee(request.user, task):
            return Response(
                JSONResponse.PERMISSION_DENIED,
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

