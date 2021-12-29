from django import forms
from .models import Order, ChangeTeacherRequestt, Complains
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
        fields =['Reason']
class complainsForm(forms.ModelForm):
    class Meta:
        model = Complains
        fields =['Regards','Reason']


