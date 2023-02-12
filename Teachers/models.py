from django.db import models
from .formatChecker import ContentTypeRestrictedFileField

# Create your models here.
from django.db.models.signals import post_save

from Notifs.models import Inboxnotif
from users.models import account


class TeacherProfile(models.Model):
    user = models.OneToOneField(account, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    Balance = models.FloatField(default=0.00,blank=True)
    docfile = ContentTypeRestrictedFileField(upload_to="cvs",content_types=['application/pdf' ],max_upload_size=5242880,blank=False, null=False)
    Experience = models.TextField(max_length=5000, blank=True)
    qualifications1 = models.CharField(max_length=2000)
    qualifications2 = models.CharField(max_length=2000, blank=True)
    qualifications3 = models.CharField(max_length=2000, blank=True)
    qualifications4 = models.CharField(max_length=2000, blank=True)
    IBAN =models.CharField(max_length=23, blank=True)
    BankName = models.CharField(max_length=100, blank=True)
    BankCountry = models.CharField(max_length=100, blank=True)
    specialzed_courses1 = models.CharField(max_length=200)
    specialzed_courses2 = models.CharField(max_length=200, blank=True)
    specialzed_courses3 = models.CharField(max_length=200, blank=True)
    grades = models.CharField(max_length=200, blank=True)
    Notes = models.TextField(max_length=5000, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_Regicted = models.BooleanField(default=False)
    __original_is_accepted = None

    @property
    def docfile_url(self):

        if self.docfile and hasattr(self.docfile, 'url'):
            return self.docfile.url
        else:
            self.user_img = ''
            return self.user_img
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_is_accepted = self.is_accepted

    def notify(sender,instance,*args,**kwargs):
        TeacherProfile = instance

        if TeacherProfile.is_accepted:
            if TeacherProfile.is_accepted != TeacherProfile.__original_is_accepted:
                Message = 'congrats,your profile accepted.'
                notifs = Inboxnotif(sender=TeacherProfile.user,recipient=TeacherProfile.user,Message=Message,notif_type=2)
                notifs.save()
                usrerStaff =  account.objects.get(id=TeacherProfile.user.id)
                usrerStaff.is_staff = True
                usrerStaff.save(update_fields=['is_staff'])
            elif TeacherProfile.is_Regicted:
                Message = 'sorry,your profile Rejected.'
                notifs = Inboxnotif(sender=TeacherProfile.user, recipient=TeacherProfile.user, Message=Message,notif_type=2)
                notifs.save()
    def __str__(self):
        return '{} {}'.format(self.user.first_name,self.user.last_name)
post_save.connect(TeacherProfile.notify,sender=TeacherProfile)

class paid(models.Model):
    Teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    recived = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Teacher.user.first_name


