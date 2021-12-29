from django.contrib import admin
from .models import course, RatingReview


# Register your models here.
class courseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('course_name',)}
    list_display = ( 'course_name','img')
admin.site.register(course,courseAdmin)
admin.site.register(RatingReview)

