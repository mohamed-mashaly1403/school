
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render


# Create your views here.
from courses.models import RatingReview, course,Price









def courses(request):
    courses = course.objects.filter( is_active=True).order_by('id')
    price = Price.objects.all()[0].coursePrice


    Paginatorr = Paginator(courses, 3)
    page = request.GET.get('page')
    paged_courses = Paginatorr.get_page(page)
    # # x = range(1, Paginatorr.num_pages)
    # # courses_count = courses.count()

    context = {
               'courses': paged_courses,
                'price': price,
               # 'courses_count':  courses_count,
               # 'x': x

               }
    return render(request,'courses.html',context)
# class courseListView(ListView):
#     model = course
#     paginate_by = 3
#     template_name = "courses.html"


def courseDetails(request,course_name):
    courseDets = course.objects.get(slug__iexact=course_name)
    price = Price.objects.all().order_by('courseClasses')
    price1st = Price.objects.all()[0].coursePrice
    reviews = RatingReview.objects.filter(course__slug=course_name, status=True).order_by('updated_date')
    rates=[]
    courseTeacher = courseDets.teacher
    youtubeUrl=courseDets.youtubeUrl

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
               'count':count,
               'courseTeacher':courseTeacher,
               'price': price,
               'price1st':price1st,
               'youtubeUrl':youtubeUrl
               }
    return render(request, 'course-details.html',context)
def search(request):
    courses=""
    courses_count=0
    keyword=""
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword != '':
            courses = course.objects.order_by('-slug').filter(Q(is_active=True) , Q(description__icontains= keyword) | Q(description_ar__icontains= keyword) | Q(course_name__icontains= keyword)| Q(course_name_ar__icontains= keyword))
            courses_count = courses.count()
        else:
            courses =''
            courses_count = 0
    # else:
    #     courses = course.objects.order_by('-slug').filter(course_name__icontains= 'Emsat')
    #     courses_count = courses.count()
    #     keyword = 'Emsat'
    context = {
        'courses': courses,
        'courses_count': courses_count,
        'keyword':keyword

    }
    return render(request,'courses.html',context)
def searchHome(request,keyword):
    if keyword != '':
        courses = course.objects.order_by('-slug').filter(Q(is_active=True) ,
            Q(description__icontains=keyword) | Q(description_ar__icontains=keyword) | Q(course_name__icontains=keyword) | Q(course_name_ar__icontains=keyword))
        courses_count = courses.count()
    else:
        courses = ''
        courses_count = 0
    context = {
        'courses': courses,
        'courses_count': courses_count,
        'keyword': keyword

    }

    return render(request, 'courses.html', context)
def pricing (request):
    price = Price.objects.all().order_by('courseClasses')

    # print(price[0].courseClasses)
    # print(price[0].coursePrice)
    # print(price[0].privEN.all())
    context = {
        'price': price,


    }
    return render(request, 'pricing.html',context )

