import math
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import django.core.mail


# Create your views here.
from django.template.loader import render_to_string

from Notifs.models import Inboxnotif
from Teachers.form import TeacherProfileForm, orderPoductClassesForm
from Teachers.models import TeacherProfile, paid
from courses.models import course
from orders.form import complainsForm, ChangeTeacherRequestForm, orderPoductForm
from orders.models import orderPoduct, Complains, Order, orderPoductClasses, ChangeTeacherRequestt
from users.forms import UserForm
from .form import MakeMyCourseForm
from django.utils.text import slugify


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
        print(total)
        total_to_recieve =orderPoduct.objects.filter(teacher__user=request.user.id,is_deliverd=True).aggregate(total_price=Sum('product_price'))
        print(total_to_recieve)
        recivedd = paid.objects.filter(Teacher__user=request.user.id).aggregate(total_Recived=Sum('recived'))
        print(recivedd)
        if recivedd['total_Recived'] == None:
            recived_total = 0
            print(recived_total)
        else:
            recived_total = recivedd['total_Recived']

        try:
            Balance = float(total['total_price'])* 0.7
            print(Balance)
            total_to_recieve = float(total_to_recieve['total_price']* 0.7)
            print(f'total_to_recieve{total_to_recieve}')


        except:
            Balance=0
            total_to_recieve=0
        try:
            Balance_to_recieve = float(total_to_recieve-recived_total)


        except:
            Balance_to_recieve = 0

        context = {
            'orders_count': orders_count,
            'orders': orders,
            'active_orders_count': active_orders_count,
            ' active_orders': active_orders,
            'Balance':math.floor(Balance),
            'Balance_to_recieve':math.floor(Balance_to_recieve)
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
    total_to_recieve = orderPoduct.objects.filter(teacher__user=request.user.id, is_deliverd=True).aggregate(total_price=Sum('product_price'))
    recivedd = paid.objects.filter(Teacher__user=request.user.id).aggregate(total_Recived=Sum('recived'))
    try:
        Balance = float(total['total_price']) * 0.7
        total_to_recieve = float(total_to_recieve['total_price'] * 0.7)

    except:
        Balance = 0
        total_to_recieve = 0

    try:
        print(recivedd['total_Recived'])
        if recivedd['total_Recived'] == None:
            recived_total = 0
        else:
            recived_total = recivedd['total_Recived']
        Balance_to_recieve = float(total_to_recieve - recived_total)

    except:
        Balance_to_recieve = 0
    if request.method == 'POST':
        amount = request.POST['amount']
        print(amount)
        bank_data = TeacherProfile.objects.get(user=request.user)
        if bank_data.IBAN and bank_data.BankName and bank_data.BankCountry:
            messages.success(request, _('Money will be added to your Bank account soon'))
            mail_subject = 'Teacher withdraw Request'
            mail_body = render_to_string('teachers/teacherwithdrawemail.html', {
                'user': request.user.email,
                'Amount': amount,

            })
            to_email = 'Vschool.com@gmail.com'
            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
            send_mail.send()
            return redirect('TeacherDashboard')
        else:
            messages.error(request, _('Your bank account details missing!'))
            return redirect('Teacheredit_profile')
    context = {

        'Balance': Balance,
        'Balance_to_recieve': math.floor(Balance_to_recieve)
    }

    return render(request, 'teachers/withdrawRequest.html',context)


@login_required(login_url='login')
def teacherProfile(request):
        Inboxnotif.objects.filter(recipient=request.user,notif_type=2).delete()
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
                    if form.cleaned_data['docfile'] != None:
                        print(form.cleaned_data['docfile'].size)
                        if form.cleaned_data['docfile'].size <= 2097152:
                            animal = form.save(commit=False)
                            animal.user = request.user
                            animal.save()
                            messages.success(request, _('Your Account will be reviewed and will back to you soon'))
                            mail_subject = 'Teacher registration'
                            mail_body = render_to_string('teachers/teacherRegistrationMail.html', {
                                'user': request.user.email,

                            })
                            to_email = 'first_man@windowslive.com'
                            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
                            send_mail.send()
                            return render(request, 'teachers/waitForReview.html')
                        else:
                            messages.error(request, _('file bigger than 2 MB'))
                    else:
                        messages.error(request, _('cv can not be empty!'))
                else:
                    messages.error(request, _('Your cv file not pdf'))
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
            messages.success(request, _('Complain has submited and will be intouch with you very soon'))
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
            if user_form.cleaned_data['user_img'] == None:
                if Profile_form.cleaned_data['docfile'] == None:
                    user_form.save()
                    Profile_form.save()
                    messages.success(request, _('profile updated'))
                    return redirect('Teacheredit_profile')
                else:
                    if Profile_form.cleaned_data['docfile'].size > 2097152:
                        messages.error(request, _('Your CV bigger than 2 MB'))
                    else:
                        user_form.save()
                        Profile_form.save()
                        messages.success(request, _('profile updated'))
                        return redirect('Teacheredit_profile')
            else:
                if user_form.cleaned_data['user_img'].size > 1048576:
                    messages.error(request, _('Your photo bigger than 1 MB'))
                    user_form.save(commit=False)
                elif Profile_form.cleaned_data['docfile'] != None:
                    if Profile_form.cleaned_data['docfile'].size > 2097152:
                        messages.error(request, _('Your CV bigger than 2 MB'))
                    else:
                        user_form.save()
                        Profile_form.save()
                        messages.success(request, _('profile updated'))
                        return redirect('Teacheredit_profile')
                else:
                    user_form.save()
                    Profile_form.save()
                    messages.success(request, _('profile updated'))
                    return redirect('Teacheredit_profile')
        else:
            messages.error(request, _('Your cv file is not pdf'))

    else:
        user_form = UserForm(instance=request.user)
        Profile_form = TeacherProfileForm(instance=teacherProfile)

    context = {
        'user_form': user_form,
        'Profile_form': Profile_form
    }
    return render(request, 'teachers/Teacheredit_profile.html', context)
@user_passes_test(lambda u: u.is_staff)
def TeacherCourseDetails(request,order_id):
    Inboxnotif.objects.filter(recipient=request.user, notif_type=3).delete()
    order_detail = orderPoduct.objects.get(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    total_urls = orderPoductClasses.objects.filter(order__order_number=order_id).order_by('updated_at')
    urls_notDeliverd = orderPoductClasses.objects.filter(order__order_number=order_id,class_url_is_deliverd=False)
    urls_Deliverd = orderPoductClasses.objects.filter(order__order_number=order_id,class_url_is_deliverd=True)
    form = orderPoductForm(instance=order_detail)
    urls_count = total_urls.count()
    left = order.total_classes - urls_Deliverd.count()
    context = {
        'order_detail': order_detail,
        'order': order,
        'urls': total_urls,
        'form':form,
        'urls_count':urls_count,
        'urlss':urls_Deliverd,
        'urls_notDeliverd':urls_notDeliverd,
        'left':left
    }
    return render(request, 'teachers/TeacherCourseDetails.html', context)
@user_passes_test(lambda u: u.is_staff)
def RejectCourse(request,order_id):
    url = request.META.get('HTTP_REFERER')
    form = ChangeTeacherRequestForm(request.POST)

    if request.method == 'POST':
        current_user = request.user
        if form.is_valid():
            data = ChangeTeacherRequestt()
            data.Reason = form.cleaned_data['Reason']
            data.ip = request.META.get('REMOTE_ADDR')
            data.user_id = request.user.id
            data.order_id = order_id
            data.save()
            messages.success(request, _('request has submited and will change soon'))
            mail_subject = 'Reject course from teacher'
            mail_body = render_to_string('orders/emailToChangeTeacher.html', {
                'user': current_user.email,
                'order_number': data.order_id,
                'Reason': data.Reason,


            })
            to_email = 'first_man@windowslive.com'
            send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
            send_mail.send()
        else:
            print('not vaild')

        return redirect(url)
@user_passes_test(lambda u: u.is_staff)
def submit_courseUrl(request,order_id):
    url = request.META.get('HTTP_REFERER')


    if request.method == 'POST':
        # try:
        #     reviews = orderPoductClasses.objects.get(order_id=order_id)
        #     form = orderPoductClassesForm(request.POST,instance=reviews)
        #     form.save()
        #     messages.success(request,'review has updated')
        #     return redirect(url)

        # except orderPoductClasses.DoesNotExist:
        form = orderPoductClassesForm(request.POST)
        print(form.errors)
        if form.is_valid():
            data = orderPoductClasses()
            data.class_url = form.cleaned_data['class_url']

            data.classTime = form.cleaned_data['classTime']
            data.order_id = order_id
            data.save()
            messages.success(request, _('url has submited'))
        else:
            print('not vaild')

        return redirect(url)
@user_passes_test(lambda u: u.is_staff)
def submit_courseMaterial(request,order_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = orderPoduct.objects.get(order_id=order_id)
            form = orderPoductForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,_('Url has updated'))
            return redirect(url)

        except orderPoductClasses.DoesNotExist:
            form =orderPoductForm(request.POST)
            print(form.errors)
            if form.is_valid():
                form.save()
                messages.success(request, _('url2 has submited'))
            else:
                print('not vaild')

            return redirect(url)
@user_passes_test(lambda u: u.is_staff)
def lessonDone(request,order_id):
    url = request.META.get('HTTP_REFERER')
    order = Order.objects.get(id=order_id)
    order_detail = orderPoduct.objects.get(order__id=order_id)
    if request.method == 'POST':
        class_urlL = request.POST['class_urlL']
        reviews = orderPoductClasses.objects.get(id=class_urlL)
        form = orderPoductClassesForm(request.POST,instance=reviews)
        print(form.errors)
        if form.is_valid():

            reviews.class_url_is_deliverd = form.cleaned_data['class_url_is_deliverd']
            reviews.save(update_fields=['class_url_is_deliverd'])
            messages.success(request, _('url has submited'))
            urls = orderPoductClasses.objects.filter(order__id=order_id,class_url_is_deliverd=True)
            urls_count = urls.count()
            print(urls_count)
            print(order.total_classes)
            if urls_count >= order.total_classes:
                order_detail.is_deliverd = True
                order_detail.save(update_fields=['is_deliverd'])
                order.status = True
                order.save(update_fields=['status'])

            else:
                print('test')
        else:
            print('not vaild')
        return redirect(url)
@user_passes_test(lambda u: u.is_staff)
def changeDate(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        class_urlL = request.POST['class_urlL']
        reviews = orderPoductClasses.objects.get(id=class_urlL)
        form = orderPoductClassesForm(request.POST,instance=reviews)
        print(form.errors)
        if form.is_valid():

            reviews.classTime = form.cleaned_data['classTime']
            reviews.class_url = form.cleaned_data['class_url']
            try:
                if  reviews.class_url and not reviews.classTime :
                    reviews.save(update_fields=['class_url'])
                    messages.success(request, _('new class url has submitted'))
                elif reviews.classTime and not reviews.class_url:
                    reviews.save(update_fields=['classTime'])
                    messages.success(request, _('new class timing has submitted'))
                elif reviews.classTime and reviews.class_url:
                    reviews.save(update_fields=['classTime','class_url'])
                else:
                    messages.error(request, _('New Date or url can not be empty '))

            except:
                messages.success(request, _('New Date or url can not be empty '))

        else:
            print('not vaild')
        return redirect(url)
@user_passes_test(lambda u: u.is_staff)
def MakeMyCourse(request):


    # TeacherMakeMyCourseForm = MakeMyCourseForm(instance=request.user)
    # context = {
    #     'TeacherMakeMyCourseForm': TeacherMakeMyCourseForm,
    #
    # }
    # return render(request, 'teachers/makeMyCourse.html', context)
    try:
        teacher = TeacherProfile.objects.get(user=request.user.id)
    except:
        messages.error(request, _('No teacher profile for the user'))
        return redirect('TeacherDashboard')

    TeacherMakeMyCourseForm = MakeMyCourseForm(request.POST, request.FILES)

    if request.method == 'POST':
        if TeacherMakeMyCourseForm.is_valid():

            if TeacherMakeMyCourseForm.cleaned_data['img'] != None:
                if TeacherMakeMyCourseForm.cleaned_data['img'].size > 1048576:
                    messages.error(request, _('Your photo bigger than 1 MB'))
                    TeacherMakeMyCourseForm.save(commit=False)
                else:
                    TeacherMakeMyCourseForm.save(commit=True)
                    course_name = TeacherMakeMyCourseForm.cleaned_data['course_name']
                    name= course.objects.get(course_name=course_name)
                    name.teacher = teacher
                    name.slug = slugify(TeacherMakeMyCourseForm.cleaned_data['course_name'])

                    name.save(update_fields=['teacher','slug'])
                    messages.success(request, _('course created and will show up in courses after review'))
                    mail_subject = 'Teacher create course'
                    mail_body = f"review course {course_name} for teacher {teacher}"
                    to_email = 'Vschool.com@gmail.com'
                    send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
                    send_mail.send()
                    return redirect('courses')
            else:
                TeacherMakeMyCourseForm.save(commit=False)
                messages.error(request, _('course image required'))
                return redirect('MakeMyCourse')
        else:

            print(TeacherMakeMyCourseForm.errors)
    else:
        TeacherMakeMyCourseForm = MakeMyCourseForm()


    context = {
        'TeacherMakeMyCourseForm': TeacherMakeMyCourseForm,

    }
    return render(request, 'teachers/makeMyCourse.html', context)
@user_passes_test(lambda u: u.is_staff)
def editMyCourse(request):
    try:
        teacher = TeacherProfile.objects.get(user=request.user.id)
    except:
        messages.error(request, _('No teacher profile for the user'))
        return redirect('TeacherDashboard')
    TeacherCourses = course.objects.filter(teacher=teacher)

    context = {
        'TeacherCourses': TeacherCourses,

    }
    return  render(request, 'teachers/teasherDashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def editCourse(request , id):
    courseProfile = get_object_or_404(course, id=id)

    if request.method == 'POST':
        TeacherMakeMyCourseForm = MakeMyCourseForm(request.POST, request.FILES,instance=courseProfile)
        if TeacherMakeMyCourseForm.is_valid():

            if TeacherMakeMyCourseForm.cleaned_data['img'] != None:
                if TeacherMakeMyCourseForm.cleaned_data['img'].size > 1048576:
                    messages.error(request, _('Your photo bigger than 1 MB'))
                    TeacherMakeMyCourseForm.save(commit=False)
                else:
                    TeacherMakeMyCourseForm.save(commit=True)
                    messages.success(request, _('course updated successfully'))
                    return redirect('courses')
            else:
                TeacherMakeMyCourseForm.save(commit=False)
                messages.error(request, _('course image required'))
                return redirect('editCourse')
        else:

            print(TeacherMakeMyCourseForm.errors)
    else: TeacherMakeMyCourseForm = MakeMyCourseForm(instance=courseProfile)

    context = {
        'TeacherMakeMyCourseForm': TeacherMakeMyCourseForm,
        'id':id,

            }
    return render(request, 'teachers/makeMyCourse.html', context)









