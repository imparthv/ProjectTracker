from django.db import models
from django.conf import settings


STATUS = [
    ("STARTED", "started"),
    ("IN_PROGRESS", "in progress"), 
    ("REVIEW", "review"),
    ("ENDED", "ended"),
]
class Project(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS, default="STARTED")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_projects"
    )
    project_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="members",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


