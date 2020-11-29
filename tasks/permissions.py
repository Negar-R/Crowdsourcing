import functools

from django.http import HttpResponse
from accounts.models import UserProfile


def is_agent(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        print(request.user.id)
        if request.user.userprofile.user_type == UserProfile.AGENT:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse("Permission Denied", status=403)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    return wrapper
