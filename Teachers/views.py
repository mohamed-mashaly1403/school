from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import django.core.mail

# Create your views here.
from django.template.loader import render_to_string

from Teachers.form import TeacherProfileForm
from Teachers.models import TeacherProfile, paid
from orders.form import complainsForm
from orders.models import orderPoduct, Complains
from users.forms import UserForm


def TeacherDashboard(request):
    accepted = TeacherProfile.objects.filter(is_accepted=True, user=request.user).exists()
    if accepted:
        if request.user.is_staff:
            pass
        else:
            request.user.is_staff= True
            request.user.save()
        orders = orderPoduct.objects.filter(teacher__user=request.user.id)
        active_orders = orderPoduct.objects.filter(teacher__user=request.user.id, is_deliverd=False)
        orders_count = orders.count()
        active_orders_count = active_orders.count()
        total =orderPoduct.objects.filter(teacher__user=request.user.id).aggregate(total_price=Sum('product_price'))
        recivedd = paid.objects.filter(Teacher__user=request.user.id).aggregate(total_Recived=Sum('recived'))

        try:
            Balance = float(total['total_price'])* 0.7

        except:
            Balance=0
        try:
            Balance_to_recieve = float(Balance-recivedd['total_Recived'])

        except:
            Balance_to_recieve = 0

        context = {
            'orders_count': orders_count,
            'orders': orders,
            'active_orders_count': active_orders_count,
            ' active_orders': active_orders,
            'Balance':Balance,
            'Balance_to_recieve':Balance_to_recieve
        }
        return render(request, 'teachers/teasherDashboard.html', context)
    else:
        Regected = TeacherProfile.objects.filter(is_Regicted=True, user=request.user).exists()
        if Regected:

            return render(request, 'teachers/regicted.html')
        else:

            return render(request, 'teachers/waitForReview.html')

@user_passes_test(lambda u: u.is_staff)
def AskForWithdraw(request):
    total = orderPoduct.objects.filter(teacher__user=request.user.id).aggregate(total_price=Sum('product_price'))
    recivedd = paid.objects.filter(Teacher__user=request.user.id).aggregate(total_Recived=Sum('recived'))
    try:
        Balance = float(total['total_price']) * 0.7

    except:
        Balance = 0
    try:
        Balance_to_recieve = float(Balance - recivedd['total_Recived'])

    except:
        Balance_to_recieve = 0
    if request.method == 'POST':
        amount = request.POST['amount']
        print(amount)
        bank_data = TeacherProfile.objects.get(user=request.user)
        if bank_data.IBAN and bank_data.BankName and bank_data.BankCountry:
            messages.success(request, 'Money will be added to your Bank account soon')
            mail_subject = 'Teacher withdraw Request'
            mail_body = render_to_string('teachers/teacherwithdrawemail.html', {
                'user': request.user.email,
                'Amount': amount,

            })
            to_email = 'first_man@windowslive.com'
            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
            send_mail.send()
            return redirect('TeacherDashboard')
        else:
            messages.error(request, 'Your bank account details missing!')
            return redirect('Teacheredit_profile')
    context = {

        'Balance': Balance,
        'Balance_to_recieve': Balance_to_recieve
    }

    return render(request, 'teachers/withdrawRequest.html',context)


@login_required(login_url='login')
def teacherProfile(request):
        have_account = TeacherProfile.objects.filter(user=request.user).exists()
        if have_account:
            accepted = TeacherProfile.objects.filter(is_accepted=True, user=request.user).exists()
            Regected = TeacherProfile.objects.filter(is_Regicted=True, user=request.user).exists()
            if accepted:
                return redirect('TeacherDashboard')
            else:
                if Regected:

                    return render(request, 'teachers/regicted.html')
                else:

                    return render(request, 'teachers/waitForReview.html')

        else:
            if request.method == 'POST':
                form = TeacherProfileForm(request.POST,request.FILES)
                print(form.errors)
                if form.is_valid():
                    animal = form.save(commit=False)
                    animal.user = request.user
                    animal.save()
                    messages.success(request, 'Your Account will be reviewed and will back to you soon')
                    mail_subject = 'Teacher registration'
                    mail_body = render_to_string('teachers/teacherRegistrationMail.html', {
                        'user': request.user.email,

                    })
                    to_email = 'first_man@windowslive.com'
                    send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
                    send_mail.send()
                    return render(request, 'teachers/waitForReview.html')
                else:
                    print('not vaild')
            else:
                print('not post')
                form = TeacherProfileForm()
            context = {
                'form': form
            }

            return render(request, 'teachers/teacherRegister.html', context)
@user_passes_test(lambda u: u.is_staff)
def Teachercomplains(request):
    url = request.META.get('HTTP_REFERER')
    form = complainsForm(request.POST)

    if request.method == 'POST':
        current_user = request.user
        if form.is_valid():
            data = Complains()
            data.Reason = form.cleaned_data['Reason']
            data.ip = request.META.get('REMOTE_ADDR')
            data.user_id = request.user.id
            data.Regards = form.cleaned_data['Regards']
            data.save()
            messages.success(request, 'Complain has submited and will be intouch with you very soon')
            mail_subject = 'Teacher Complain'
            mail_body = render_to_string('orders/emailComplain.html', {
                'user': current_user.email,
                'Regards': data.Regards,
                'Reason': data.Reason,

            })
            to_email = 'first_man@windowslive.com'
            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
            send_mail.send()
        else:
            print('not vaild')

        return redirect(url)
    return render(request,'teachers/Teachercomplains.html')

@user_passes_test(lambda u: u.is_staff)
def TeacherOrders(request):
    active_orders = orderPoduct.objects.filter(teacher__user=request.user.id).order_by('is_deliverd')

    context = {
        'active_orders': active_orders,
    }

    return render(request, 'teachers/TeacherOrders.html', context)
@user_passes_test(lambda u: u.is_staff)
def TeacherActiveOrders(request):
    active_orders = orderPoduct.objects.filter(teacher__user=request.user.id, is_deliverd=False)
    context = {
        'active_orders': active_orders,
    }
    return render(request, 'teachers/TeacherOrders.html', context)
@user_passes_test(lambda u: u.is_staff)
def ReceivedInstallments(request):
    installments = paid.objects.filter(Teacher__user=request.user.id).order_by('-created_at')
    totalInstallments = paid.objects.filter(Teacher__user=request.user.id).aggregate(totalInstall=Sum('recived'))
    try:
        total_recived = float(totalInstallments['totalInstall'])

    except:
        total_recived = 0

    context = {
        'installments': installments,
        'total_recived':total_recived,
    }
    return render(request, 'teachers/recivedInstallments.html', context)
@user_passes_test(lambda u: u.is_staff)
def Teacheredit_profile(request):
    try:
        teacherProfile = get_object_or_404(TeacherProfile, user=request.user)
    except:
        user_form = UserForm(instance=request.user)
        Profile_form = TeacherProfileForm()
        context = {
            'user_form': user_form,
            'Profile_form': Profile_form
        }
        return render(request, 'teachers/Teacheredit_profile.html', context)

    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        Profile_form = TeacherProfileForm(request.POST,request.FILES, instance=teacherProfile)
        if user_form.is_valid() and Profile_form.is_valid():
            user_form.save()
            Profile_form.save()
            messages.success(request, 'profile updated')
            return redirect('Teacheredit_profile')
    else:
        user_form = UserForm(instance=request.user)
        Profile_form = TeacherProfileForm(instance=teacherProfile)

    context = {
        'user_form': user_form,
        'Profile_form': Profile_form
    }
    return render(request, 'teachers/Teacheredit_profile.html', context)


