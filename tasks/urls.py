from django.urls import path
from tasks.views import (AddTask, getAllTask, getReportedTask, getAssignTask,
                         assignTask)

# app_name = 'tasks'

urlpatterns = [
    path('add_task', AddTask.as_view(), name='add_task'),
    path('all_task', getAllTask, name='all_task'),
    path('reported_task', getReportedTask, name='reported_task'),
    path('assigned_task', getAssignTask, name='assigned_task'),
    path('task_assign', assignTask, name='task_assign'),
]
