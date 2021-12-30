from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import django.core.mail
# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import requests

from orders.models import Order, orderPoduct
from .forms import regForm, UserForm, UserProfileForm
from .models import account, UserProfile


def register(request):
    url = request.META.get('HTTP_REFERER')
    try:
        if request.user.is_authenticated:
            return redirect(url)
    except:
        return redirect('home')
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
            # send mail to customer
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
            messages.success(request,
                             'Thank you for being one of us. please activate your account by clicking on activation url in your email')

            return redirect('/users/login/?command=verification&email=' + email)
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
    url = request.META.get('HTTP_REFERER')
    try:
        if request.user.is_authenticated:
            return redirect(url)
    except:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        try:
            auth.login(request, user)
            messages.success(request, ' successfully login ')

        except(AttributeError):
            messages.error(request, 'Wrong email or password ')
            return redirect('login')
        try:
            url = request.META.get('HTTP_REFERER')
            query = requests.utils.urlparse(url).query

            params = dict(x.split('=') for x in query.split('&'))

            if 'next' in params:
                nextPage = params['next']
                return redirect(nextPage)
        except:

            return redirect('dashboard')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'successfully Logout ')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user_profile = UserProfile(
            user=user
        )
        user_profile.save()

        messages.success(request, 'successfully activated ')
        return redirect('edit_profile')
    else:
        messages.error(request, 'invaild link')
        return redirect('register')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if account.objects.filter(email=email).exists():
            user = account.objects.get(email__iexact=email)
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
            messages.success(request, 'Click on the link on reset password mail  sent to you')
            return redirect('forgotpassword')
        else:
            messages.error(request, "account does not exist")
            return redirect(request, 'login')
    return render(request, 'accounts/forgotpassword.html')


def resetPasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Reset your Password')
        return redirect('resetPassordPage')
    else:
        messages.error(request, 'Reset password link expired')
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
            messages.success(request, 'new password has set')
            return redirect('login')

        else:
            messages.error(request, 'confirm Password does not match')
            return redirect('resetPassordPage')
    else:

        return render(request, 'accounts/resetPassordPage.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        user = account.objects.get(username__exact=request.user.username)
        if new_password == confirm_new_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'password changed successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'invalid current password ')
                return redirect('change_password')
        else:
            messages.error(request, 'new password and confirmed password do not match')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    active_orders = orderPoduct.objects.filter(user_id=request.user.id, is_deliverd=False)
    orders_count = orders.count()
    active_orders_count = active_orders.count()
    UnPaidOrders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=False)[:3:-1]
    UnPaidOrder = len(UnPaidOrders)
    context = {
        'orders_count': orders_count,
        'orders': orders,
        'active_orders_count': active_orders_count,
        ' active_orders': active_orders,
        'UnPaidOrders': UnPaidOrder
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def myOrders(request):
    active_orders = orderPoduct.objects.filter(user_id=request.user.id).order_by('is_deliverd')
    context = {
        'active_orders': active_orders,
    }

    return render(request, 'accounts/myOrders.html', context)


@login_required(login_url='login')
def myActiveOrders(request):
    active_orders = orderPoduct.objects.filter(user_id=request.user.id, is_deliverd=False)
    context = {
        'active_orders': active_orders,
    }
    return render(request, 'accounts/myOrders.html', context)


@login_required(login_url='login')
def UnPaidOrders(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=False)[:3:-1]

    context = {
        'UnPaidOrders': orders,
    }
    return render(request, 'accounts/UnPaidOrders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    try:
        userProfile = get_object_or_404(UserProfile, user=request.user)
    except:
        user_form = UserForm(instance=request.user)
        Profile_form = UserProfileForm()
        context = {
            'user_form': user_form,
            'Profile_form': Profile_form
        }
        return render(request, 'accounts/edit_profile.html', context)

    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        Profile_form = UserProfileForm(request.POST, instance=userProfile)
        if user_form.is_valid() and Profile_form.is_valid():
            user_form.save()
            Profile_form.save()
            messages.success(request, 'profile updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        Profile_form = UserProfileForm(instance=userProfile)

    context = {
        'user_form': user_form,
        'Profile_form': Profile_form
    }
    return render(request, 'accounts/edit_profile.html', context)
@login_required(login_url='login')
def deltePhoto(request):
    dd =account.objects.get(id=request.user.id)
    dd.user_img.delete()
    dd.user_img= ''
    dd.save(update_fields=['user_img'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))








