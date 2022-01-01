from django.contrib import admin

# Register your models here.
from Teachers.models import TeacherProfile, paid

admin.site.register(TeacherProfile)
class paidAdmin(admin.ModelAdmin):
    list_display = ['Teacher','recived','created_at']
admin.site.register(paid,paidAdmin)
