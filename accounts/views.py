import uuid
from datetime import timedelta

from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError

from Crowdsourcing.settings import EMAIL_HOST_USER
from accounts.models import UserProfile
from accounts.redis_exe import Redis
# Create your views here.


class Registeration(View):
    name = 'register'
    
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if User.objects.filter(email=email).exists():
            err_msg = "There ia one account with this email,\
                        Please select another one."
            context = {
                'err_msg': err_msg
            }
            return render(request, 'accounts/register.html', context=context)
        try:
            user, created = User.objects.get_or_create(username=username,
                                                       email=email)
        except IntegrityError:
            err_msg = "There ia one account with this username,\
                        Please select another one."
            context = {
                'err_msg': err_msg
            }
            return render(request, 'accounts/register.html', context=context)
        
        if not created:
            err_msg = "There is one user with this username, \
                       please select another one"
            context = {
                'err_msg': err_msg
            }
            return render(request, 'accounts/register.html', context=context)
        else:
            user.set_password(password)
            user.save()

            #TODO: use signal
            profile, created = UserProfile.objects.get_or_create(user=user,
                                                                 user_type=user_type)
            sendingEmail(request, user.id, email)

            data = "Verification code was sent for your email. \
                    Please confirm it to login"
            context = {
                'data': data
            }
            return render(request, 'show_message.html', context=context)


class Login(View):
    name = 'login'

    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        
        # (authenticate): verify a set of credentials and return user
        try:
            user = User.objects.get(email=email)
            print("AUTHENTICATE : ", user)
            sendingEmail(request, user.id, email)
            data = "Verification code was sent for your email. \
                Please confirm it to login"
            context = {
                'data': data
            }
            return render(request, 'show_message.html', context=context)
        except User.DoesNotExist:
            return redirect('register')
        

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('all_task')
    else:
        return redirect('login')


def sendingEmail(request, user_id, user_email):
    uuid_code = str(uuid.uuid4())
    Redis.add(user_id, timedelta(minutes=5), uuid_code)

    subject = 'Verify your CROWD SOURCING account'
    message = 'Follow this link to verify your account'

    reverse_generated_link = reverse(
        'verify', kwargs={'send_code': f"{user_id}+{uuid_code}"})
    link = f"{request.get_host()}{reverse_generated_link}"
    send_message = f"{message}:\t{link}"

    try:
        send_mail(subject, send_message, EMAIL_HOST_USER, [user_email],
                  fail_silently=False)
    except Exception as e:
        data = "Sending email to you was failed."
        context = {
            'data': data
        }
        return render(request, 'show_message.html', context=context)


def verify(request, send_code):
    try:
        user_id = send_code.split('+')[0]
        uuid = send_code.split('+')[1]
        original_uuid = Redis.get_user(user_id).decode('utf-8')
        if original_uuid:
            # (login): saves the user’s ID in the session, \
            # using Django’s session framework.
            if uuid == original_uuid:
                user = User.objects.get(id=user_id)
                login(request, user)
                return redirect('all_task')
            else:
                data = "Login Failed"
                context = {
                    'data': data
                }
                return render(request, 'show_message.html', context=context)
        else:
            data = "Your verification code was expired"
            context = {
                'data': data
            }
            return render(request, 'show_message.html', context=context)

    except UserProfile.DoesNotExist:
        data = "Login Failed"
        context = {
            'data': data
        }
        return render(request, 'show_message.html', context=context)
