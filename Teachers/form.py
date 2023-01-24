from django import forms

from Teachers.models import TeacherProfile
from orders.models import orderPoductClasses
from courses.models import course


class TeacherProfileForm(forms.ModelForm):
    docfile = forms.FileField(required=False,error_messages = {'invalid':("pdf files only")},widget=forms.FileInput)

    class  Meta:
        model = TeacherProfile
        fields = '__all__'
        exclude = ['Balance','is_accepted','user','is_Regicted']

    # def clean_file(self):
    #     file = self.cleaned_data.get("docfile", False)
    #     filetype = magic.from_buffer(file.read())
    #     if not "pdf" in filetype:
    #         raise forms.ValidationError("File is not pdf.")
    #     return file

    def __init__(self, *args, **kwargs):
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
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
        fields = ['is_school_subject','course_name', 'course_name_ar', 'language1', 'language1_tr','language2','language2_tr','typeEN','typeAR','description','description_ar','img','is_active']

    def __init__(self, *args, **kwargs):
        super(MakeMyCourseForm, self).__init__(*args, **kwargs)

        self.fields['course_name'].widget.attrs['pattern'] = "[A-Za-z]"
        for field in self.fields :
            if not self.fields[field] == self.fields['is_school_subject']:
                self.fields[field].widget.attrs['class'] = 'form-control'

