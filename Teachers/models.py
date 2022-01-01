from django.db import models

# Create your models here.

from users.models import account


class TeacherProfile(models.Model):
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

    @property
    def docfile_url(self):

        if self.docfile and hasattr(self.docfile, 'url'):
            return self.docfile.url
        else:
            self.user_img = ''
            return self.user_img

    def __str__(self):
        return self.user.first_name
class paid(models.Model):
    Teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    recived = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Teacher.user.first_name


