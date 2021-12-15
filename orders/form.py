from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','country','city','grade','Curriculum_type','term','order_note']