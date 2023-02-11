from django import forms
from .models import Order, ChangeTeacherRequestt, Complains, orderPoduct
from courses.models import RatingReview


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['country','city','grade','Curriculum_type','term','order_note','quantity','order_course_language']

class RatingReviewForm(forms.ModelForm):
    class Meta:
        model = RatingReview
        fields =['subject','review','rating']
class ChangeTeacherRequestForm(forms.ModelForm):
    class Meta:
        model = ChangeTeacherRequestt
        fields =['Reason','type']
class complainsForm(forms.ModelForm):
    class Meta:
        model = Complains
        fields =['Regards','Reason']
class orderPoductForm(forms.ModelForm):
    class Meta:
        model = orderPoduct
        fields =['class_material_url']
    def __init__(self, *args, **kwargs):
        super(orderPoductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


