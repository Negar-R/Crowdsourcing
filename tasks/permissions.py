import functools

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from accounts.models import UserProfile


def is_agent(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.userprofile.user_type == UserProfile.AGENT:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    return wrapper
