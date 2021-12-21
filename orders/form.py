from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['country','city','grade','Curriculum_type','term','order_note','quantity','order_course_language']