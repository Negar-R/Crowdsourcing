from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate
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

        print("Get Posted data !!! ")
        user, created = User.objects.get_or_create(username=username,
                                                   email=email)
        print("user careated !!! ")
        if not created:
            return HttpResponse("There is one user with this username, \
                                please use another one")
        user.set_password(password)
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        sendingEmail(request, email, str(profile.verification_uuid))

        return HttpResponse("Your verification code was sent for you")


class Login(View):
    name = 'login'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'accounts/login.html')
        else:
            return HttpResponse("salam")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.id
            request.session.set_expiry(300)
            return HttpResponse("You are logged in")
        else:
            return HttpResponse("You should be registered first")


def Logout(request):
    try:
        del request.session['user_id']
        request.session.clear_expired()
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


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


#TODO: redirect to login page
def verify(request, uuid):
    try:
        user_profile = UserProfile.objects.get(verification_uuid=uuid,
                                               is_verified=False)
    except UserProfile.DoesNotExist:
        return HttpResponse("User does not exist or is already verified")
    user_profile.is_verified = True
    user_profile.save()
    # return redirect(request, 'accounts/login.html')
    return HttpResponse("Your accounts was verified, now you can login")
