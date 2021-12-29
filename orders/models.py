from django.db import models

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
    # teacher = models.ForeignKey(teachers,on_delete=models.SET_NULL,blank=True,null=True) to add after teacher moduel
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deliverd = models.BooleanField(default=False)
    class_material_url =models.URLField(max_length=200, blank=True)


    def __str__(self):
        return self.order.order_course.course_name
class orderPoductClasses(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    class_url = models.URLField(max_length=200, blank=True)
    class_url_is_deliverd = models.BooleanField(default=False)
    classTime = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
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
    




