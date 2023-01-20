from django.shortcuts import render
from django.db.models import Count

from courses.models import course, Price
from orders.models import orderPoduct


def handler404(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response
def home(request):
    courses = orderPoduct.objects.values_list('order_course__course_name').annotate(course_count=Count('order_course')).order_by('-course_count')[:3]
    orderrr=[a_tuple[0] for a_tuple in courses]
    price = Price.objects.all()[0].coursePrice

    cour = []
    for i in orderrr:

        orderr = course.objects.get(course_name=i)
        cour.append(orderr)
    print(cour)

    context = {
        'cour': cour,
        'nbar': 'home',
        'price':price

    }
    return render(request,'home.html',context)

