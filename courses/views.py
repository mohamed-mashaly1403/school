from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from .models import course


def courses(request):
    courses = course.objects.all().filter( is_active=True).order_by('id')
    Paginatorr = Paginator(courses, 6)
    page = request.GET.get('page')
    paged_courses = Paginatorr.get_page(page)
    x = range(1, Paginatorr.num_pages)
    courses_count = courses.count()

    context = {
               'courses': paged_courses,
               'courses_count':  courses_count,
               'x': x

               }
    return render(request,'courses.html',context)
def courseDetails(request,course_name):
    courseDets = course.objects.get(slug__iexact=course_name)
    context = {'courseDets': courseDets,

               }
    return render(request, 'course-details.html',context)
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword != '':
            courses = course.objects.order_by('-slug').filter(Q(description__icontains= keyword) | Q(course_name__icontains= keyword))
            courses_count = courses.count()
        else:
            courses =''
            courses_count = 0
    context = {
        'courses': courses,
        'courses_count': courses_count,
        'keyword':keyword,
    }
    return render(request,'courses.html',context)
