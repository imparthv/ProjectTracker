from django.db import models
from django.conf import settings
from projects.models import Project

STATUS = [
    ("ENDED", "ended"),
    ("REVIEW", "review"),
    ("IN_PROGRESS", "in progress"),     
    ("STARTED", "started")
]

PRIORITY=[
    ("HIGH","high"),
    ("MEDIUM","medium"),
    ("LOW","low")
]
class Task(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS, default="STARTED")
    priority = models.CharField(max_length=15, choices=PRIORITY, default="LOW")
    assigned_project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
        related_name = "allocated_tasks"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_tasks"
    )

      # Person responsible for task
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assigned_tasks",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
