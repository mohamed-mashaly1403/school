from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.backends import django
import django.core.mail

from .form import OrderForm
from courses.models import course
from .models import Order, Payment, orderPoduct
import datetime
from django.core.mail import EmailMessage
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
            print(data.Curriculum_type)
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
                'total': data.total,
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







