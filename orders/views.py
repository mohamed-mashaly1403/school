from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.backends import django
import django.core.mail

from Notifs.models import Inboxnotif

from .form import OrderForm, RatingReviewForm, ChangeTeacherRequestForm, complainsForm
from courses.models import course, RatingReview
from .models import Order, Payment, orderPoduct, orderPoductClasses, ChangeTeacherRequestt, Complains
import datetime

from django.template.loader import render_to_string

# Create your views here.
@login_required(login_url='login')
def place_order(request,needed_course_id,price,lessons):
      if request.method == 'POST':
        current_user = request.user


        print(price)
        form = OrderForm(request.POST)

        ncourse = course.objects.get(id=needed_course_id)
        print(ncourse)

        if form.is_valid():
            print(form.errors)

            data = Order()
            data.first_name = request.user.first_name
            data.last_name = request.user.last_name
            data.phone = request.user.phone
            data.country = form.cleaned_data['country']
            data.quantity = form.cleaned_data['quantity']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.user = current_user
            data.grade = form.cleaned_data['grade']
            data.Curriculum_type = form.cleaned_data['Curriculum_type']
            data.order_course = ncourse
            try:
                data.total_classes = data.quantity * lessons
            except(TypeError):
                data.total_classes=1

            data.term = form.cleaned_data['term']
            data.order_course_language = form.cleaned_data['order_course_language']
            data.total = price
            if data.total == 0:
                data.tax = 0
                data.gtotal = 0
            else:
                data.tax = (data.total * data.quantity) * 0.05
                data.gtotal = (data.total * data.quantity) + data.tax
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%d%m')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'needed_course': data.order_course,
                'ctotal': data.total_classes,
                'tax': data.tax,
                'Gtotal': data.gtotal,
                'lessons': data.total_classes,
                'price': data.total,

            }

            return render(request, 'orders/payments.html', context)

        else:
            print('not vaild')
            print(form.errors)
            return redirect('courses')
@login_required(login_url='login')
def Editplaceorder(request,order_number):
    order = Order.objects.get(order_number=order_number)
    print(order)
    context = {
        'order': order,
        'needed_course': order.order_course,
        'ctotal': order.total_classes,
        'tax': order.tax,
        'Gtotal': order.gtotal,
        'lessons': order.total_classes,
        'price': order.total,

    }

    return render(request, 'orders/payments.html', context)


@login_required(login_url='login')
def checkout (request,slug='',lessons=0, price=0):
    needed_course = course.objects.filter(slug=slug).first()
    lang = ['Arabic','English','Quran','French','Chinese']

    context = {
        'price': price,
        'needed_course': needed_course,
        'needed_course_id':needed_course.id,
        'lessons': lessons,
        'lang':lang

    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def payments(request):
    current_user = request.user
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=current_user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user=current_user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        status=body['status'],
        amount_paid=order.gtotal,

    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    orderPoductt = orderPoduct()
    orderPoductt.order_id = order.id
    orderPoductt.payment = payment
    orderPoductt.user_id = current_user.id
    orderPoductt.order_course = order.order_course
    orderPoductt.quantity = order.quantity
    orderPoductt.product_price = order.gtotal
    orderPoductt.ordered = True
    orderPoductt.save()
    Order.objects.filter(user=current_user,is_ordered=False).delete()
    # send mail to customer
    mail_subject = 'Congratulation your order has set successfully'
    mail_body = render_to_string('orders/orderset.html', {
        'user': current_user,
        'order_number': order,
        'tlessons':order.total_classes

    })
    to_email = current_user.email
    send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
    send_mail.send()
    # ========================== email to super admin
    mail_subject = 'Congratulation your order has set successfully,someone make payment'
    mail_body = render_to_string('orders/orderset.html', {
        'user': current_user,
        'order_number': order,
        'tlessons': order.total_classes

    })

    send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=['first_man@windowslive.com'])
    send_mail.send()
    #============================================================
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }


    return JsonResponse(data)
@login_required(login_url='login')
def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        order_Poduct = orderPoduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=payment_id)



        context={
            'order':order,
            'order_Poduct':order_Poduct,
            'order_number':order_number,
            'payment_id':payment,
            'Sub_Total':order.gtotal
        }
        return render(request, 'orders/order_complete.html', context)
    except(Order.DoesNotExist,Payment.DoesNotExist):
        return redirect('home')
@login_required(login_url='login')
def order_details(request,order_id):
    Inboxnotif.objects.filter(recipient=request.user, notif_type=4).delete()
    order_detail = orderPoduct.objects.get(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    urls = orderPoductClasses.objects.filter(order__order_number=order_id).order_by('updated_at')
    reviews = RatingReview.objects.all().filter(order__order_number=order_id,status=True)
    urls_Deliverd = orderPoductClasses.objects.filter(order__order_number=order_id,class_url_is_deliverd=True)
    left = order.total_classes - urls_Deliverd.count()


    print(reviews)
    context={
        'order_detail':order_detail,
        'order': order,
        'urls':urls,
        'reviews':reviews,
        'left':left
    }
    return render(request,'orders/order_course-details.html',context)
@login_required(login_url='login')
def submit_review(request,course_id,order_id):
    url = request.META.get('HTTP_REFERER')


    if request.method == 'POST':
        try:
            reviews = RatingReview.objects.get(user__id=request.user.id,course__id=course_id,order__id=order_id)
            form = RatingReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,_('review has updated'))
            return redirect(url)

        except RatingReview.DoesNotExist:
            form = RatingReviewForm(request.POST)
            if form.is_valid() :
                data = RatingReview()


                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.course_id = course_id
                data.user_id = request.user.id
                data.order_id = order_id
                data.save()
                messages.success(request, _('review has submited'))
            else:
                print('not vaild')

            return redirect(url)
@login_required(login_url='login')
def ChangeTeacherRequest(request,order_id):
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
            mail_subject = 'Request to change teacher'
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
def complains(request):
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
            mail_subject = 'Complain'
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
    return render(request,'accounts/complains.html')













