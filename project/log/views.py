from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

# Activate mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError


from .utils import TokenGenerator, generate_token

# Email
from django.core.mail import EmailMessage
from django.conf import settings


import threading


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, 'log/signup.html')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken")
            return render(request, 'log/signup.html')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken")
            return render(request, 'log/signup.html')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        email_subject = "Activate your Account"
        message = render_to_string('log/activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })
        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
        EmailThread(email_message).start()
        messages.info(request, "Activate your account by clicking the link sent to your email")
        return redirect('loginn')

    return render(request, 'log/signup.html')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account activated successfully")
            return redirect('loginn')

        return render(request, 'log/activatefail.html')


def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']
        myuser = authenticate(username=username, password=password)

        if myuser is not None:
            login(request, myuser)
            return render(request, 'base.html')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('loginn')

    return render(request, 'log/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('loginn')


class reset(View):
    def get(self,request):
        return render(request,'log/reset.html')
    