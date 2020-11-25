from django.urls import path
from accounts.views import index


urlpatterns = [
    path('inedx', index, name='index')
]
