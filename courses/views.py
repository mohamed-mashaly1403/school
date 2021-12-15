from django.shortcuts import render

# Create your views here.
from .models import course


def courses(request):
    courses = course.objects.all().filter( is_active=True).order_by('id')

    context = {'courses': courses,

               }
    return render(request,'courses.html',context)
def courseDetails(request,course_name):
    courseDets = course.objects.get(slug__iexact=course_name)
    context = {'courseDets': courseDets,

               }
    return render(request, 'course-details.html',context)