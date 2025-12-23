from django.db import models
from django.conf import settings


STATUS = [
    ("ENDED", "ended"),
    ("REVIEW", "review"),
    ("IN_PROGRESS", "in progress"),     
    ("STARTED", "started")
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


