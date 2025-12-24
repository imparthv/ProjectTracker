from django.urls import path, include
from . import views

urlpatterns = [
    # Creating user api
     path('users/all/', views.ListAllAccountsView.as_view(), name='list-users'),
    path('users/me/', views.UserAccountView.as_view(), name='user-details'),
    path('users/register/', views.UserAccountRegisterView.as_view(), name='user-registration'),

    # Creating project api
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-info'),
    path('projects/myprojects/', views.UserProjectsView.as_view(), name='user-projects'),

    # Creating task api
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-info'),
    path('user/mytasks/', views.UserTasksView.as_view(), name='user-task'),
]