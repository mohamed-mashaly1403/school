from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
import django.core.mail
# Create your views here.
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.utils.encoding import force_bytes
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import requests

from Notifs.models import Inboxnotif
from orders.models import Order, orderPoduct
from .forms import regForm, UserForm, UserProfileForm, MessageForm
from .models import account, UserProfile, Inbox


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
            mail_subject = 'myschool.site- please activate your account'
            mail_body = render_to_string('accounts/emailActivation.html', {
                'user': user,
                'current_site': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
            send_mail.send()
            messages.success(request,_('Thank you for registration with us,YOUR ACCOUNT HAS BEEN CREATED! ,Please, verify it by clicking the activation link that has been sent to your email.If the email doesn\'t appear shortly, please be sure to check your spam'))

            return redirect('/users/login/?command=verification&email=' + email)
            # return redirect('home')

        else:
            print('not vaild')
    else:

        form = regForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

# def glogin(request):
#     user = account._default_manager.filter(is_active=False ).order_by('-joined_date')[0]
#     user.is_active = True
#     user.save()
#     return redirect('login')
def login(request):
    url = request.META.get('HTTP_REFERER')
    try:
        if request.user.is_authenticated:
            return redirect(url)
    except:
        return redirect('login')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        try:
            auth.login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, _('successfully login'))

        except(AttributeError):
            messages.error(request, _('Wrong email or password or account not activated '))
            return redirect('login')
        try:
            url = request.META.get('HTTP_REFERER')
            query = requests.utils.urlparse(url).query

            params = dict(x.split('=') for x in query.split('&'))

            if 'next' in params:
                nextPage = params['next']
                return redirect(nextPage)
        except:
            if request.user.is_authenticated and not request.user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('TeacherDashboard')
    else:
        try:
            user = account._default_manager.filter(is_active=False,is_admin=False,is_staff=False).order_by('-joined_date')[0]
            if user.has_usable_password():
                return render(request, 'accounts/login.html')
            else:
                auth.login(request, user, backend='social_core.backends.google.GoogleOAuth2')
                user.is_active = True
                user.save()

                return redirect('home')
        except: return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')
# for google login======================
# @login_required
# def homeg(request):
#     if request.user.is_authenticated:
#         return render(request, 'home.html')
#     else:
#         pass

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, _('successfully Logout'))
    return redirect('home')


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

        messages.success(request, _('successfully activated'))
        return redirect('edit_profile')
    else:
        messages.error(request, _('invaild link'))
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
            messages.success(request, _('Click on the link on reset password mail  sent to you'))
            return redirect('forgotpassword')
        else:
            messages.error(request, _("account does not exist"))
            # return redirect(request, 'login')
    return render(request, 'accounts/forgotpassword.html')


def resetPasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, _('Reset your Password'))
        return redirect('resetPassordPage')
    else:
        messages.error(request, _('Reset password link expired'))
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
            messages.success(request, _('new password has set'))
            return redirect('login')

        else:
            messages.error(request, _('confirm Password does not match'))
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
                messages.success(request, _('password changed successfully'))
                return redirect('change_password')
            else:
                messages.error(request, _('invalid current password'))
                return redirect('change_password')
        else:
            messages.error(request, _('new password and confirmed password do not match'))
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
    active_orders = orderPoduct.objects.filter(user_id=request.user.id).order_by('is_deliverd','-created_at')
    context = {
        'active_orders': active_orders,
    }

    return render(request, 'accounts/myOrders.html', context)


@login_required(login_url='login')
def myActiveOrders(request):
    active_orders = orderPoduct.objects.filter(user_id=request.user.id, is_deliverd=False).order_by('-created_at')
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
            if user_form.cleaned_data['user_img'] != None:
                if user_form.cleaned_data['user_img'].size > 1048576:
                    messages.error(request, _('Your photo bigger than 1 MB'))
                    user_form.save(commit=False)
                else:
                    user_form.save()
                    Profile_form.save()
                    messages.success(request, _('profile updated'))
                    return redirect('edit_profile')

            else:
                user_form.save()
                Profile_form.save()
                messages.success(request, _('profile updated'))
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

@login_required(login_url='login')
def inbox(request):
    user = request.user
    messageRequests=user.messages.filter(is_receiver_delete=False)
    allmeesagescount = messageRequests.count()

    unreadCount = messageRequests.filter(is_read=False).count()
    sent = user.sentMessages.filter(is_sender_delete=False)
    sent_count = sent.filter(sender=user).count()
    allsentcount = sent.count()

    context = {'messageRequests': messageRequests,
               'unreadCount': unreadCount,
               'sent':sent,
               'sent_count':sent_count,
               'allmeesagescount': allmeesagescount,
               'allsentcount': allsentcount,
               }
    return render(request, 'accounts/inbox.html', context)
@login_required(login_url='login')
def viewMessage(request, pk):
    uu = request.META['HTTP_REFERER']

    if '/users/inbox/' not in uu:
        Inboxnotif.objects.filter(recipient=request.user,message_id=pk).delete()

    user = request.user
    messageRequests = user.messages.filter(is_receiver_delete=False)

    unreadCount = messageRequests.filter(is_read=False).count()
    try:

        message = user.messages.get(id=pk)

    except:
        message = user.sentMessages.get(id=pk)
    try:
        order = Order.objects.get(order_number=message.order)
        course = order.order_course
    except:
        order=''
        course=''
    if message.is_read == False:
        message.is_read = True
        Inboxnotif.objects.filter(recipient=request.user, message_id=pk).delete()
        message.save()
    context = {'message': message,'order':order,'course':course,'unreadCount':unreadCount}
    return render(request, 'accounts/read_email.html', context)
@login_required(login_url='login')
def DeleteMessage(request, pk):
    user = request.user
    try:
        message = user.messages.get(id=pk)
        message.is_receiver_delete = True
        message.save(update_fields=['is_receiver_delete'])
        if message.is_receiver_delete and message.is_sender_delete:
            message.delete()
    except:
        message = user.sentMessages.get(id=pk)
        message.is_sender_delete = True
        message.save(update_fields=['is_sender_delete'])
        if message.is_receiver_delete and message.is_sender_delete:
            message.delete()
    return redirect('inbox')
@login_required(login_url='login')
def DeleteMessages(request):
    user = request.user

    if request.method == 'POST':
        try:
            checked_items = request.POST.getlist("toDelete")
            for i in checked_items:
                try:
                    message = user.messages.get(id=i)
                    message.is_receiver_delete = True
                    message.save(update_fields=['is_receiver_delete'])

                except:
                    message = user.sentMessages.get(id=i)
                    message.is_sender_delete = True
                    message.save(update_fields=['is_sender_delete'])
                if message.is_receiver_delete and  message.is_sender_delete :
                    message.delete()
        except:
            return redirect('inbox')

    return redirect('inbox')

@login_required(login_url='login')
def createMessage(request,pk):
    user = request.user
    messageRequests = user.messages.filter(is_receiver_delete=False)
    unreadCount = messageRequests.filter(is_read=False).count()
    sender = user
    try:
        ordr = Order.objects.get(id=pk)
        recipient = ordr.user
        subject = f'Hi,I am {user.first_name} your teacher for {ordr.order_course} course- order no. {ordr.order_number}'
        form = MessageForm(initial={'recipient': recipient, 'subject': subject})

    except:
        form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        print(form.errors)

        if form.is_valid():
            message = form.save(commit=False)

            if message.recipient == request.user:
                messages.error(request, _('Your can not sent to your self!'))

            else:
                message.sender = sender
                recipient = message.recipient
                message.save()


                messages.success(request, _('Your message was successfully sent!'))
                return redirect('inbox')
    context = { 'form': form,'unreadCount':unreadCount}
    return render(request, 'accounts/message_form.html', context)
@login_required(login_url='login')
def createMessagefromStudent(request,pk):
    user = request.user
    messageRequests = user.messages.filter(is_receiver_delete=False)
    unreadCount = messageRequests.filter(is_read=False).count()


    ordr = orderPoduct.objects.get(id=pk)
    recipient = ordr.teacher.user
    subject = f'Hi,I am {user.first_name} Student of {ordr.order_course} course- order no. {ordr.order.order_number}'
    form = MessageForm(initial={'recipient': recipient, 'subject': subject})


    context = { 'form': form,'unreadCount':unreadCount}
    return render(request, 'accounts/message_form.html', context)

def reply(request,pk):
    try:
        message = get_object_or_404(Inbox, id=pk)
        sender = message.sender
        body = f"\n \n\n \n==================================================\n \n{sender}\n \n{message.created.strftime('%d/%m/%Y %H:%M')}\n \n{message.body} "
        form = MessageForm(instance=message,initial={'recipient': sender,'body':body})

    except:
        form = MessageForm()


    context = {
        'form': form,


    }
    return render(request, 'accounts/message_form.html', context)







