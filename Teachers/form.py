from django import forms

from Teachers.models import TeacherProfile
from orders.models import orderPoductClasses
from courses.models import course
from django.utils.translation import gettext as _
class TeacherProfileForm(forms.ModelForm):
    docfile = forms.FileField(required=False,error_messages = {'invalid':("pdf files only")},widget=forms.FileInput)

    class  Meta:
        model = TeacherProfile
        fields = '__all__'
        exclude = ['Balance','is_accepted','user','is_Regicted']

    def __init__(self, *args, **kwargs):
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        self.fields['country'].widget.attrs['placeholder'] = _('Country you live in')
        self.fields['city'].widget.attrs['placeholder'] = _('City you live in')
        self.fields['qualifications1'].widget.attrs['placeholder'] = _('1st Academic degree(required)')
        self.fields['qualifications2'].widget.attrs['placeholder'] = _('2nd Academic degree(optional)')
        self.fields['qualifications3'].widget.attrs['placeholder'] = _('3rd Academic degree(optional)')
        self.fields['qualifications4'].widget.attrs['placeholder'] = _('4th Academic degree(optional)')
        self.fields['specialzed_courses1'].widget.attrs['placeholder'] = _('1st subject you teach(required)')
        self.fields['specialzed_courses2'].widget.attrs['placeholder'] = _('2nd subject you teach(optional)')
        self.fields['specialzed_courses3'].widget.attrs['placeholder'] = _('3rd subject you teach(optional)')
        self.fields['grades'].widget.attrs['placeholder'] = _('Grades you teach.')
        self.fields['IBAN'].widget.attrs['placeholder'] = _('Bank IBAN')
        self.fields['BankName'].widget.attrs['placeholder'] = _('Bank Name')
        self.fields['BankCountry'].widget.attrs['placeholder'] = _('Bank Country')
        self.fields['Experience'].widget.attrs['placeholder'] = _('Recap your Experience')
        self.fields['Notes'].widget.attrs['placeholder'] = _('Any thing you want to say about yourself')

        # for field in self.fields.values():
        #     field.widget.attrs['placeholder'] = _(field.label)
class orderPoductClassesForm(forms.ModelForm):
    class Meta:
        model = orderPoductClasses
        fields =['class_url','class_url_is_deliverd','classTime']
    def __init__(self, *args, **kwargs):
        super(orderPoductClassesForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
class MakeMyCourseForm(forms.ModelForm):
    img = forms.ImageField(required=True,error_messages = {'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model = course
        fields = ['is_school_subject','course_name', 'course_name_ar', 'language1','language2','typeEN','typeAR','description','description_ar','img','is_active','youtubeUrl','courseGrades','country']

    def __init__(self, *args, **kwargs):
        super(MakeMyCourseForm, self).__init__(*args, **kwargs)
        self.fields['youtubeUrl'].widget.attrs['placeholder'] = 'youtube url'
        self.fields['youtubeUrl'].widget.attrs['pattern'] = 'https://www.youtube.com/embed/.*'
        self.fields['youtubeUrl'].widget.attrs['oninvalid'] = "this.setCustomValidity('requested format: https://www.youtube.com/embed/.*')"
        self.fields['courseGrades'].widget.attrs['required'] = "required"
        self.fields['typeEN'].widget.attrs['required'] = "required"
        self.fields['typeEN'].widget.attrs['onchange'] = "yesnoCheckk(this);"
        self.fields['typeAR'].widget.attrs['required'] = "required"
        self.fields['country'].widget.attrs['required'] = "required"


        for field in self.fields :
            if not self.fields[field] == self.fields['is_school_subject']:
                self.fields[field].widget.attrs['class'] = 'form-control'

