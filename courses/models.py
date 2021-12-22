from django.db import models
from django.urls import reverse

# Create your models here.
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
    def __str__(self):
        return self.course_name


