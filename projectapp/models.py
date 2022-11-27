import uuid

from django.db import models


# Create your models here.

# import taskapp.models

class Project(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True)
    user = models.ForeignKey("taskapp.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    details = models.TextField(default="")
    is_active = models.BooleanField(default=True, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)
    started = models.BooleanField(default=False, null=True, blank=True)
    started_on = models.DateTimeField(auto_now_add=False)
    completed_on = models.DateTimeField(auto_now_add=False, null=True, blank=True)
