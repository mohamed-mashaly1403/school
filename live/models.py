from django.db import models

# Create your models here.
from django.db.models.signals import post_save

from Notifs.models import Inboxnotif
from orders.models import Order, orderPoduct


class CloseLive(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __int__(self):
        return self.order

    def notify(sender, instance, *args, **kwargs):
        CloseLive = instance
        teacher = orderPoduct.objects.get(order=instance.order)
        Message = f'{teacher.order_course} meeting start.'

        notifs = Inboxnotif(sender=teacher.teacher.user, recipient=instance.order.user,message_id=CloseLive.order, Message=Message, notif_type=4) #to delete
        notifs.save()




post_save.connect(CloseLive.notify,sender=CloseLive)

