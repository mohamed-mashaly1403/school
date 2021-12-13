from django.db import models

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
    # notes = models.TextField(max_length=200,blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.course_name


