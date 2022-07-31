from django import forms

from Teachers.models import TeacherProfile
from orders.models import orderPoductClasses


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
