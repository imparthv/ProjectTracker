from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "created_at", "assigned_project","owner", "assigned_to",]
    search_fields = ["name", "owner", "assigned_project" ]
