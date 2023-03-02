from django.shortcuts import render
from django.db.models import Count

from Teachers.models import TeacherProfile
from courses.models import course, Price
from orders.models import orderPoduct
from users.models import account, Vists
import datetime


def handler404(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response
def handler500(request, *args, **argv):
    context = {"test":"testt"}
    response = render(request,'errors/500.html',  context=context)
    response.status_code = 500
    return response
def home(request):
    courses = orderPoduct.objects.values_list('order_course__course_name').annotate(course_count=Count('order_course')).order_by('-course_count')[:3]
    orderrr=[a_tuple[0] for a_tuple in courses]
    price = Price.objects.all()[0].minn
    trainers = TeacherProfilee.objects.filter(is_accepted=True).count()
    course_count = course.objects.filter(is_active=True).count()
    students_count = account.objects.filter(is_active=True,is_staff=False).count()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if Vists.objects.filter(ip=ip,created__gt=datetime.date.today()).exists():
        pass
    else:
        Vists(ip=ip).save()
    visits_count = Vists.objects.all().count()




    cour = []
    for i in orderrr:

        orderr = course.objects.get(course_name=i)
        cour.append(orderr)
    print(cour)

    context = {
        'cour': cour,
        'nbar': 'home',
        'price':price,
        'trainers':trainers,
        'course_count':course_count,
        'students_count':students_count,
        'visits_count':visits_count


    }
    return render(request,'home.html',context)

