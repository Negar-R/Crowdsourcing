from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TaskModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    value = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True)
