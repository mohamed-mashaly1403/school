
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render


# Create your views here.
from courses.models import RatingReview, course


def courses(request):
    courses = course.objects.filter( is_active=True).order_by('id')

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
    reviews = RatingReview.objects.filter(course__slug=course_name, status=True).order_by('updated_date')
    rates=[]
    for i in reviews:
        rates.append(i.rating)
    try:
        avg=sum(rates)/len(rates)
        count = len(rates)
    except:
        avg=0
        count=0

    Paginatorr = Paginator(reviews, 6)
    page = request.GET.get('page')
    paged_review = Paginatorr.get_page(page)
    x = range(1, Paginatorr.num_pages)
    reviews_count = reviews.count()
    context = {'courseDets': courseDets,
               'reviews':reviews,
               'reviews_count': reviews_count,
               'paged_review': paged_review,
               'x': x,
               'avg':avg,
               'count':count
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
