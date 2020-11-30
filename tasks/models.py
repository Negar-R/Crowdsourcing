from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TaskModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    value = models.PositiveIntegerField()
    estimation = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='reporters')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 related_name='assignees', blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.title}"
