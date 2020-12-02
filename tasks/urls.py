from django.urls import path
from tasks.views import (AddTask, getAllTask, getReportedTask, getAssignedTask,
                         assignTask, seeDescription)

# app_name = 'tasks'

urlpatterns = [
    path('add_task', AddTask.as_view(), name='add_task'),
    path('all_task', getAllTask, name='all_task'),
    path('reported_task', getReportedTask, name='reported_task'),
    path('assigned_task', getAssignedTask, name='assigned_task'),
    path('task_assign', assignTask, name='task_assign'),
    path('see_description/<int:task_id>', seeDescription,
         name='see_description'),
]
