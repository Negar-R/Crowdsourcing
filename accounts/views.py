import uuid
import logging
from datetime import timedelta

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.generic import View
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout


from Crowdsourcing.redis_exe import Redis
from accounts.models import UserProfile
from Crowdsourcing.settings import EMAIL_HOST_USER
# Create your views here.

logger = logging.getLogger(__name__)


class Registeration(View):
    name = 'register'
    
    def get(self, request):
        logger.debug("GET request method to registration view")
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
            logger.info("Duplicate email : {}".format(email))

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

            logger.info("Duplicate username : {}".format(username))

            return render(request, 'accounts/register.html', context=context)
        
        if not created:
            err_msg = "There is one user with this username, \
                       please select another one"
            context = {
                'err_msg': err_msg
            }

            logger.info("Duplicate username : {}".format(username))

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

            # It is not recommended to log user sensitive data
            logger.info("New profile with {} username was created".
                        format(username))

            return render(request, 'show_message.html', context=context)


class Login(View):
    name = 'login'

    def get(self, request):
        logger.debug("get request method to login view")
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        
        try:
            user = User.objects.filter(email=email).values('id', 'email')
            sendingEmail(request, user[0]['id'], user[0]['email'])
            data = "Verification code was sent for your email. \
                Please confirm it to login"
            context = {
                'data': data
            }

            logger.info("login email sent to user with email: {}".format(email))

            return render(request, 'show_message.html', context=context)
        except (User.DoesNotExist, IndexError):
            logger.info("user with email: {} does not exist".format(email))
            return redirect('register')
        

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        logger.info("user with username: {} logged out"
                    .format(request.user.username))
        return redirect('all_task')
    else:
        return redirect('login')


def sendingEmail(request, user_id, user_email):
    uuid_code = str(uuid.uuid4())
    Redis.add(user_id, timedelta(minutes=5), uuid_code)

    subject = 'Verify your CROWDSOURCING account'
    message = 'Follow this link to verify your account'

    reverse_generated_link = reverse(
        'verify', kwargs={'send_code': f"{user_id}+{uuid_code}"})
    link = f"{request.get_host()}{reverse_generated_link}"
    send_message = f"{message}:\t{link}"

    try:
        send_mail(subject, send_message, EMAIL_HOST_USER, [user_email],
                  fail_silently=False)
        logger.info("email was sent to user with email: {}".format(user_email))
    except Exception as e:
        data = "Sending email to you was failed."
        context = {
            'data': data
        }

        logger.error("sendig email to {} was failed".format(user_email))
        logger.error(e)

        return render(request, 'show_message.html', context=context)


def verify(request, send_code):
    try:
        user_id = send_code.split('+')[0]
        uuid = send_code.split('+')[1]
        original_uuid = Redis.get_user(user_id)
        if original_uuid:
            original_uuid = original_uuid.decode('utf-8')
            # (login): saves the user’s ID in the session, \
            # using Django’s session framework.
            if uuid == original_uuid:
                user = User.objects.get(id=user_id)
                login(request, user)
                logger.info("user with username: {} logged in"
                            .format(user.username))
                return redirect('all_task')
            else:
                data = "Login Failed"
                context = {
                    'data': data
                }

                logger.info("uuid_code of user with id: {} was not found"
                            .format(user_id))

                return render(request, 'show_message.html', context=context)
        else:
            data = "Your verification code was expired"
            context = {
                'data': data
            }

            logger.info("uuid_code of user with id: {} was expired"
                        .format(user_id))

            return render(request, 'show_message.html', context=context)

    except UserProfile.DoesNotExist:
        data = "Login Failed"
        context = {
            'data': data
        }

        logger.info("user profile not found")

        return render(request, 'show_message.html', context=context)
