from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "created_at", "owner__username", "owner__email"]
    search_fields = ["name", "owner__username", ]
