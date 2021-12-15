from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
import django.core.mail
# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import requests


from .forms import regForm
from .models import account


def register(request):
    if request.method == 'POST':
        form = regForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.errors)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            # username = email
            user = account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               password=password, username=username)
            user.phone = phone
            user.save()
            #send mail to customer
            current_site = get_current_site(request)
            mail_subject = 'school.com please activate your account'
            mail_body = render_to_string('accounts/emailActivation.html', {
                'user': user,
                'current_site': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
            send_mail.send()
            messages.success(request,'Thank you for being one of us. please activate your account by clicking on activation url in your email')

            return redirect('/users/login/?command=verification&email='+email)
            # return redirect ('/home.html')

        else:
            print('not vaild')
    else:
        print('not post')
        form = regForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        try:
            auth.login(request,user)
            messages.success(request, ' successfully login ')

        except(AttributeError):
            messages.error(request, 'please activate your account by clicking on activation url in your email')
            return redirect('login')
        try:
            url = request.META.get('HTTP_REFERER')
            query= requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))
            if 'next' in params:
                nextPage = params['next']
                return redirect(nextPage)
        except :
            # return redirect('dashboard')
            return redirect('home')
    return render(request,'accounts/login.html')
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'successfully Logout ')
    return redirect('login')
def activate(request,uidb64,token):
     try:
         uid = urlsafe_base64_decode(uidb64).decode()
         user = account._default_manager.get(pk=uid)

     except(TypeError,ValueError,OverflowError,account.DoesNotExist):
         user = None
     if user is not None and default_token_generator.check_token(user,token):
         user.is_active = True
         user.save()
         messages.success(request,'successfully activated ')
         return redirect('login')
     else:
         messages.error(request,'invaild link')
         return redirect(request,'register')
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if account.objects.filter(email=email).exists():
            user=account.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = 'reset your password'
            mail_body = render_to_string('accounts/reset_password.html', {
                'user': user,
                'current_site': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
            send_mail.send()
            messages.success(request,'Click on the link on reset password mail  sent to you')
            return redirect('forgotpassword')
        else:
            messages.error(request,"account does not exist")
            return redirect(request,'login')
    return render(request,'accounts/forgotpassword.html')
def resetPasswordValidate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request,'Reset your Password')
        return redirect('resetPassordPage')
    else:
        messages.error(request,'Reset password link expired')
        return redirect('login')
def resetPassordPage(request):
    if request.method == 'POST':
        createPassword = request.POST['createPassword']
        confirmPassword = request.POST['confirmPassword']
        if confirmPassword == createPassword:
            uid = request.session.get('uid')
            user = account.objects.get(pk=uid)
            user.set_password(createPassword)
            user.save()
            messages.success(request,'new password has set')
            return redirect('login')

        else:
            messages.error(request,'confirm Password does not match')
            return redirect('resetPassordPage')
    else:

        return render(request,'accounts/resetPassordPage.html')
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password= request.POST['confirm_new_password']
        user = account.objects.get(username__exact=request.user.username)
        if new_password == confirm_new_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'password changed successfully')
                return redirect('change_password')
            else:
                messages.error(request,'invalid current password ')
                return redirect('change_password')
        else:
            messages.error(request,'new password and confirmed password do not match')
            return redirect('change_password')

    return render(request,'accounts/change_password.html')