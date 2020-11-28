from django.contrib import admin
from tasks.models import TaskModel
# Register your models here.

# admin.site.register(TaskModel)
@admin.register(TaskModel)
class TaskModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}