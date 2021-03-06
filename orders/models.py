from django.db import models
from django.db.models.signals import post_save
import django.core.mail
from django.utils.translation import gettext as _
from Notifs.models import Inboxnotif
from Teachers.models import TeacherProfile
from courses.models import course



# Create your models here.
from users.models import account


class Payment(models.Model):
    user = models.ForeignKey(account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.payment_id
class Order(models.Model):
    status = (
        ('new','new'),
        ('accepted','accepted'),
        ('completed','completed'),
        ('canceled','canceled')
    )

    user = models.ForeignKey(account, on_delete=models.SET_NULL, null=True)
    order_course = models.ForeignKey(course, on_delete=models.CASCADE,blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20,unique=True)
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=15,blank=True)
    country = models.CharField(max_length=10, default='else')
    city = models.CharField(max_length=50,blank=True)
    grade = models.IntegerField( blank=True,default=1,null=True)
    quantity  = models.IntegerField( blank=True,default=1)
    Curriculum_type = models.CharField(max_length=20, blank=True, default='general')
    term = models.CharField(max_length=20, blank=True,default='first')
    total = models.FloatField(blank=True)
    tax = models.FloatField()
    gtotal = models.FloatField(default=0.00)
    total_classes = models.IntegerField(default=1, blank=True)
    status = models.CharField(max_length=10, choices=status, default='new')
    order_course_language=models.CharField(max_length=20,blank=True,default='Arabic')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_note = models.CharField(max_length=100, blank=True)



    def __str__(self):
        return self.order_number
class orderPoduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    order_course = models.ForeignKey(course,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    teacher = models.ForeignKey(TeacherProfile,on_delete=models.SET_NULL, null=True,blank=True,)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deliverd = models.BooleanField(default=False)
    class_material_url =models.URLField(max_length=200, blank=True)
    __original_teacher = None

    @property
    def Teacher_cost(self):
        return self.product_price * 0.7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_teacher = self.teacher

    def notify(sender, instance, *args, **kwargs):
        orderPoduct = instance

        if orderPoduct.teacher:
            if orderPoduct.teacher != orderPoduct.__original_teacher:
                Message = _('New student waiting')
                notifs = Inboxnotif(sender=orderPoduct.user, recipient=orderPoduct.teacher.user, Message=Message,message_id=orderPoduct.order.order_number,notif_type=3)
                notifs.save()
                stu_message =f'Teacher ready for{orderPoduct.order_course} course'
                notifss = Inboxnotif(sender=orderPoduct.teacher.user, recipient=orderPoduct.user, Message=stu_message,message_id=orderPoduct.order.order_number,notif_type=4)
                notifss.save()
                # ==================== mail to teacher
                # send mail to customer
                mail_subject = _('You got new order and your student is waiting')
                mail_body = _('Kindly go to your dashboard to proceed in the new course')
                to_email = orderPoduct.teacher.user.email
                send_mail = django.core.mail.EmailMessage(mail_subject, mail_body, to=[to_email])
                send_mail.send()
                # ==================== mail to teacher
    def __str__(self):
        return self.order.order_number
post_save.connect(orderPoduct.notify,sender=orderPoduct)
class orderPoductClasses(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    class_url = models.URLField(max_length=200, blank=True)
    class_url_is_deliverd = models.BooleanField(default=False)
    classTime = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    orders = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.order.order_number
class ChangeTeacherRequestt(models.Model):
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # teacher
    Reason = models.TextField(max_length=500,blank=True)
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.order.order_number
class Complains(models.Model):
    user = models.ForeignKey(account, on_delete=models.CASCADE)
    Regards = models.CharField(max_length=100, blank=True)
    Action_taken = models.CharField(max_length=100, blank=True,null=True)
    Reason = models.TextField(max_length=500,blank=True)
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Regards
    




