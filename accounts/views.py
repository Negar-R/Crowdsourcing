from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from Crowdsourcing.settings import EMAIL_HOST_USER, PROJECT_IP_ADDRESS
from accounts.models import UserProfile
# Create your views here.


class Registeration(View):
    name = 'register'
    
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
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

            profile, created = UserProfile.objects.get_or_create(user=user)
            sendingEmail(request, email, str(profile.verification_uuid))

            data = "Verification code was sent for your email. \
                    Please confirm it"
            context = {
                'data': data
            }
            return render(request, 'show_message.html', context=context)


class Login(View):
    name = 'login'

    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # (authenticate): verify a set of credentials and return user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.userprofile.is_verified:
                # (login): saves the user’s ID in the session, \
                # using Django’s session framework.
                login(request, user)
                return redirect('all_task')
            else:
                err_msg = "You should verify your account first"
                context = {
                    'err_msg': err_msg
                }
                return render(request, 'accounts/login.html', context=context)
        else:
            err_msg = "You should register first"
            context = {
                'err_msg': err_msg
            }
            return render(request, 'accounts/login.html', context=context)
        

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('all_task')
    else:
        return redirect('login')


#TODO:make a url correct by defining a setting variable
def sendingEmail(request, user_email, user_uuid):
    subject = 'Verify your CROWD SOURCING account'
    message = 'Follow this link to verify your account'
    reverse_generated_link = reverse('verify', kwargs={'uuid': user_uuid})
    link = f"{PROJECT_IP_ADDRESS}{reverse_generated_link}"
    send_message = f"{message}:\t{link}"

    try:
        send_mail(subject, send_message, EMAIL_HOST_USER, [user_email],
                  fail_silently=False)
    except Exception as e:
        return render(request, 'accounts/register.html')


def verify(request, uuid):
    try:
        user_profile = UserProfile.objects.get(verification_uuid=uuid)
        if user_profile.is_verified:
            return redirect('all_task')
        else:
            user_profile.is_verified = True
            user_profile.save()
            return render(request, 'accounts/login.html')

    except UserProfile.DoesNotExist:
        data = "There is no user with this verification code."
        context = {
                'data': data
            }
        return render(request, 'show_message.html', context=context)
