from django.db import models

# Create your models here.
from django.db import models

# Create your models here.



class Inboxnotif(models.Model):
    sender = models.ForeignKey('users.account', on_delete=models.SET_NULL, null=True, blank=True,related_name="sentNotif")
    recipient = models.ForeignKey('users.account', on_delete=models.SET_NULL, null=True, blank=True, related_name="recivedNotif")
    Message = models.CharField(max_length=200, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    message_id = models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return self.Message

    class Meta:
        ordering = ['is_read', '-created']