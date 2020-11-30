from django.urls import path
from django.conf.urls import url
from accounts.views import Login, Registeration, Logout, verify


# app_name = 'accounts'

urlpatterns = [
    path('register', Registeration.as_view(), name=Registeration.name),
    path('login', Login.as_view(), name=Login.name),
    path('logout', Logout, name='logout'),
    # path('verify/<str:send_code>', verify, name='verify'),
    url(r'verify/(?P<send_code>[a-z0-9\-+]+)/', verify, name='verify'),
]
