from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.exceptions import PermissionDenied

from django.db import models

from .serializers import AccountSerializer, AccountRegisterSerializer, ProjectSerializer, TaskSerializer

from accounts.models import Account
from projects.models import Project
from tasks.models import Task

# Overiding the base permission method to create a IsSuperUser Permission Class
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_superuser
        )

# List all accounts only to superuser
class ListAllAccountsView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsSuperUser]

# Creating class based view for /me/ endpoint - Shows user account of current user
class UserAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return self.request.user

# Creating class based view to register user - Registers new user
class UserAccountRegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountRegisterSerializer

# Creating class based view to view and create projects
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes  = [IsAuthenticated]

    # Shows projects only to project owner/creator or project members
    def get_queryset(self):
        return Project.objects.filter(models.Q(owner=self.request.user) | models.Q(project_members=self.request.user)) .distinct()

    # Allows only project owners to create and add project details
    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only Superusers can create a project")
        serializer.save(owner=self.request.user)
            

# Creating class based view to update specific projects
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes  = [IsAuthenticated]
    lookup_field = 'pk'   

    # Allows only project owners to change project details
    def perform_update(self, serializer):
        project = self.get_object()
        if project.owner != self.request.user:
            raise PermissionDenied("Only Project ownwers can alter project")
        else:
            serializer.save()

    # Shows project details only to project owner/creator or project members
    def get_queryset(self):
        return Project.objects.filter(models.Q(owner=self.request.user) | models.Q(project_members=self.request.user)) .distinct()
    
# Creating class based view to see user specific objects
# Shows project to only owners and the respective project members
class UserProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(models.Q(owner=self.request.user) | models.Q(project_members=self.request.user)) 
    
# Creating class based view to list tasks
class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes  = [IsAuthenticated]

    # Allows only project creators to create tasks for specific projects
    def perform_create(self, serializer):
        project = serializer.validated_data.get('assigned_project')
        if project.owner == self.request.user:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionDenied("Only project owners are allowed to create tasks!")

    # Allows only project owners and project members to see respective tasks
    def get_queryset(self):
        return Task.objects.filter(models.Q(owner=self.request.user) | models.Q(assigned_to=self.request.user)) 
    
# Creating class based view to update specific tasks
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes  = [IsAuthenticated]
    lookup_field = 'pk'    

    # Allows only task owners and member to whom tasks have been assigned to view projects
    def get_queryset(self):
        return  Task.objects.filter(models.Q(owner=self.request.user) | models.Q(assigned_to=self.request.user)) 
    
    # Allows assigned users to change task status
    def perform_update(self, serializer):
        task  = self.get_object()
        user = self.request.user
        data = serializer.validated_data

        if task.owner ==  user:
            serializer.save()
            return 
        
        elif task.assigned_to == user:
            if set(data.keys()) == {'status'}:
                serializer.save()
                return
            raise PermissionDenied("You can update only task status")
        raise PermissionDenied("Only owners can fully modify tasks")
    
    # Allows only task owners to delete tasks
    def destroy(self, request, *args, **kwargs):
        task  = self.get_object()

        if task.owner != request.user:
             raise PermissionDenied("You can update only task status")
        
        return super().destroy(request, *args, **kwargs)
        
# Creating class based view to see user specific tasks - Assigned and Created 
class UserTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes  = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(models.Q(owner=self.request.user) | models.Q(assigned_to=self.request.user)) 
