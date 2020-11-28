from django.urls import path
from tasks.views import getAllTask, AddTask

# app_name = 'tasks'

urlpatterns = [
    path('all_task', getAllTask, name='all_task'),
    path('add_task', AddTask.as_view(), name='add_task')
]
