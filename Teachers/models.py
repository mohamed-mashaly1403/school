from django.db import models

# Create your models here.
from courses.models import course
from orders.models import orderPoduct
from users.models import account


class TeacherProfile(models.Model):
    Course = models.ForeignKey(course, on_delete=models.CASCADE,blank=True, null=True)
    orders = models.ForeignKey(orderPoduct, on_delete=models.CASCADE,blank=True, null=True)
    user = models.OneToOneField(account, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20)
    Balance = models.FloatField(default=0.00,blank=True)
    docfile = models.FileField(upload_to="cvs")
    Experience = models.TextField(max_length=500, blank=True)
    qualifications1 = models.CharField(max_length=20)
    qualifications2 = models.CharField(max_length=20, blank=True)
    qualifications3 = models.CharField(max_length=20, blank=True)
    qualifications4 = models.CharField(max_length=20, blank=True)
    IBAN =models.CharField(max_length=23, blank=True)
    BankName = models.CharField(max_length=30, blank=True)
    BankCountry = models.CharField(max_length=30, blank=True)
    specialzed_courses1 = models.CharField(max_length=20)
    specialzed_courses2 = models.CharField(max_length=20, blank=True)
    specialzed_courses3 = models.CharField(max_length=20, blank=True)
    grades = models.CharField(max_length=30, blank=True)
    Notes = models.TextField(max_length=100, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_Regicted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name
