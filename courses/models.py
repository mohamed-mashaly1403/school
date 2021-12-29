from django.db import models
from django.urls import reverse
from django.db.models import Count, Avg

# Create your models here.

from users.models import account

lang =  [
    ('Arabic', 'Arabic'),
    ('English', 'English'),
    ('French', 'French'),
    ('Chinese', 'Chinese'),

]

class course(models.Model):
    course_name = models.CharField(max_length=50,unique=True)
    slug = models.CharField(max_length=100,unique=True)
    # grade = models.CharField(max_length=50)
    language1 = models.CharField(max_length=15,choices=lang,blank=False,default='')
    language2 = models.CharField(max_length=15, choices=lang, blank=False,default='')
    # teacher = models.CharField (max_length=20,blank=True)
    type = models.CharField (max_length=20,blank=False,default='General')
    description = models.TextField(max_length=500,blank=True)
    img = models.ImageField(upload_to='img/courses',blank=True)
    is_school_subject = models.BooleanField(default=True)
    # notes = models.TextField(max_length=200,blank=True)
    is_active = models.BooleanField(default=True)



    def get_url(self):
        return reverse('courseDetails', args=[self.course_name])

    def averagereview(self):
        reviews = RatingReview.objects.filter(course=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            return avg
        else:
            return 0

    def countreview(self):
        reviews = RatingReview.objects.filter(course=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
            return count
        else:
            return 0
    def orderd(self):
        reviews = orderPoduct.objects.filter(order_course=self, ordered=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
            return count
        else:
            return 0

    def __str__(self):
        return self.course_name
from orders.models import Order, orderPoduct


class RatingReview(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.course.course_name




