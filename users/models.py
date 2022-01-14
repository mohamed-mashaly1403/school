import os
from django.db import models
from django import forms
from django.db import models

# Create your models here.
#overwrite django user model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager
from django.db.models.signals import post_save

from Notifs.models import Inboxnotif
from vschool import settings


class account_manger(BaseUserManager):
    def create_user(self,first_name,last_name,email,username,password=None):
        if not email:
            raise ValueError('add your email')
        if not username:
            raise ValueError('add username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password = password
        )
        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
class account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    user_img = models.ImageField(upload_to="img/users", blank=True, default='default_avatar.png')
    #required
    joined_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','username','last_name']
    objects = account_manger()
    def __str__(self):
        return self.email
    #must mention in overwrite
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True

    @property
    def image_url(self):
        DEFAULT = 'default_avatar.png'

        if self.user_img and hasattr(self.user_img, 'url'):
            return self.user_img.url
        else:
            self.user_img = DEFAULT
            return self.user_img


    def delete(self, *args, **kwargs):
        DEFAULT = 'default_avatar.png'
        os.remove(os.path.join(settings.MEDIA_ROOT, self.user_img.name))
        self.user_img = DEFAULT
        super(account, self).delete(*args, **kwargs)






class UserProfile(models.Model):
    user = models.OneToOneField(account,on_delete=models.CASCADE)
    city = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.user.first_name

class Inbox(models.Model):
    sender = models.ForeignKey(account, on_delete=models.SET_NULL, null=True, blank=True,related_name="sentMessages")
    recipient = models.ForeignKey(account, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()

    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_sender_delete = models.BooleanField(default=False)
    is_receiver_delete = models.BooleanField(default=False)

    def notify(sender,instance,*args,**kwargs):

        Inbox = instance
        sender = Inbox.sender
        recipient = Inbox.recipient
        Message = f'{sender.first_name} sent you email.'
        notifs = Inboxnotif(sender=sender,recipient=recipient,Message=Message,message_id=Inbox.id)
        notifs.save()


    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
post_save.connect(Inbox.notify,sender=Inbox)
