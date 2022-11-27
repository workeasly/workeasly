from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from indexapp.forms import LoginForm, UserForgotPasswordForm, UserPasswordResetForm
from indexapp.tokens import account_activation_token
from taskapp.models import User
from django.core.mail import EmailMessage


def index_view(request):
    form = LoginForm()
    valuenext = request.POST.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            raw_password = form.cleaned_data.get('password')

            if "@gmail.com" in username_or_email:
                email=username_or_email.lower()
                usr=User.objects.get(email=email)
                print(usr.username)
                user=authenticate(username=usr.username,password=raw_password)
                print("log with email")
                print(user)
            else:
                user = authenticate(username=username_or_email, password=raw_password)
            if user is not None:
                login(request, user)
                request.session['username']=user.username
                request.session['password']=raw_password
                return redirect('/dashboard/')
            else:
                print("nnsndndn")
                password_error = True
        else:
            form = LoginForm(request.POST)

    if "username" in request.session and "password" in request.session:
        user = authenticate(username=request.session['username'], password=request.session['password'])
        if user:
            login(request, user)
            return redirect('/dashboard/')

    return render(request,"indexapp/index.html",locals())



def password_reset(request):

    if request.method == "POST":

        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():

            email = request.POST['email']
            if not User.objects.filter(email=email.lower()).exists():
                print(email)
                email_not_found=True
            else:

                qs = User.objects.get(email=email.lower())
                print(qs)
                qs.is_active = False
                qs.save()

                current_site = get_current_site(request)
                mail_subject = 'password reset link has been sent to your email id'
                message = render_to_string('indexapp/password_reset_mail.html', {
                    'user': qs,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(qs.pk)),
                    'token': account_activation_token.make_token(qs),
                })

                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, 'Please confirm your email address for Password reset process!')
                return redirect("/password-forgot/")

    else:
            form=UserForgotPasswordForm()
    return render(request, 'indexapp/password_forgot_form.html',locals())





def reset(request, uidb64, token):

    if request.method == 'POST':

            print("tryof rest")
            uid = force_str(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(id=uid)
            print("hello",user)

            form = UserPasswordResetForm(user=user, data=request.POST)
            print("reset form",form)
            if form.is_valid():
                print("form valid of reset")
                user.set_password(request.POST['new_password2'])
                user.is_active = True
                user.save()
                messages.success(request,'Password has been successfully updated!')
                return redirect("/")

            # else:
            #     messages.error(request,'Activation link is invalid!')

    else:
        form=UserPasswordResetForm(user=request.user)
        print(form)
    return render(request, 'indexapp/password_reset_form.html', locals())


@login_required(login_url="/")
def logout_view(request):
    logout(request)
    return  redirect("/")

from .models import Admission
from taskapp.models import ProgrammingLanguage
def apply_admission (request):
    department = ProgrammingLanguage.objects.filter(is_active=True)
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        department = request.POST['department']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        description = request.POST['description']

        Admission.objects.create(
            first_name = first_name,
            last_name=last_name,
            email=email,
            department=department,
            phone=phone,
            address=address,
            desctiption=description
        )
        
    return render(request,"admission.html",locals())