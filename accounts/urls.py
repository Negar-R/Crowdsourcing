from django.urls import path
from django.conf.urls import url
from accounts.views import Login, Registeration, Logout, verify


urlpatterns = [
    path('register', Registeration.as_view(), name=Registeration.name),
    path('login', Login.as_view(), name=Login.name),
    path('logout', Logout, name='logout'),
    url(r'verify/(?P<uuid>[a-z0-9\-]+)/', verify, name='verify'),
]
